from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView

from courses.models import Course, Enrollment, LessonProgress
from notifications.models import Notification

from .models import FeaturedTip


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:switch_role')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured_courses'] = Course.objects.filter(is_published=True)[:3]
        return ctx


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile

        enrollments = (
            Enrollment.objects.filter(user=user)
            .select_related('course')
            .annotate(lesson_total=Count('course__modules__lessons'))
        )[:4]

        recent_progress = (
            LessonProgress.objects.filter(user=user, completed=True)
            .select_related('lesson', 'lesson__module__course')
            .order_by('-completed_at')[:5]
        )

        ctx.update({
            'profile': profile,
            'enrollments': enrollments,
            'recent_progress': recent_progress,
            'recent_notifications': Notification.objects.filter(user=user)[:5],
            'course_count': Course.objects.filter(is_published=True).count(),
            'completed_count': LessonProgress.objects.filter(user=user, completed=True).count(),
        })
        return ctx


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from courses.models import Assignment, AssignmentSubmission, Exam, ExamQuestion, ExamSubmission
from analytics.models import UserActivity


@login_required
def assignments_list_view(request):
    """Lists assignments associated with courses in which the student is enrolled."""
    enrolled_courses = Course.objects.filter(enrollments__user=request.user, is_published=True)
    assignments = Assignment.objects.filter(course__in=enrolled_courses).select_related('course').order_by('due_date')
    
    # Check submissions
    submissions = AssignmentSubmission.objects.filter(user=request.user)
    submissions_dict = {sub.assignment_id: sub for sub in submissions}
    
    for a in assignments:
        a.submission = submissions_dict.get(a.id)
        
    return render(request, 'dashboard/assignments.html', {
        'assignments': assignments,
    })


@login_required
def exams_list_view(request):
    """Lists all timed MCQ certificate exams for enrolled courses."""
    enrolled_courses = Course.objects.filter(enrollments__user=request.user, is_published=True)
    exams = Exam.objects.filter(course__in=enrolled_courses, is_active=True).select_related('course').order_by('-created_at')
    
    # Check submissions
    submissions = ExamSubmission.objects.filter(user=request.user)
    submissions_dict = {sub.exam_id: sub for sub in submissions}
    
    for e in exams:
        e.submission = submissions_dict.get(e.id)
        
    return render(request, 'dashboard/exams.html', {
        'exams': exams,
    })


@login_required
def take_exam_view(request, exam_id):
    """Loads a timed MCQ exam interface with radio selection questions."""
    exam = get_object_or_404(Exam, id=exam_id, is_active=True)
    
    # Pre-check: if they already completed it, redirect them to safety
    submission = ExamSubmission.objects.filter(user=request.user, exam=exam).first()
    if submission:
        messages.info(request, "You have already completed this exam.")
        return redirect('dashboard:exams')
        
    questions = exam.questions.all().order_by('id')
    return render(request, 'dashboard/take_exam.html', {
        'exam': exam,
        'questions': questions,
    })


@login_required
@require_POST
def submit_exam_ajax(request, exam_id):
    """AJAX handler to grade ticking MCQ exam responses on-the-fly and award XP."""
    exam = get_object_or_404(Exam, id=exam_id, is_active=True)
    
    # Double submit block
    if ExamSubmission.objects.filter(user=request.user, exam=exam).exists():
        return JsonResponse({'success': False, 'error': 'Exam has already been submitted.'}, status=400)
        
    questions = exam.questions.all()
    if not questions.exists():
        return JsonResponse({'success': False, 'error': 'This exam has no questions defined.'}, status=400)
        
    correct_count = 0
    total_questions = questions.count()
    answers_json = {}
    
    for q in questions:
        # Extract selected option (A, B, C, D)
        selected = request.POST.get(f'question_{q.id}', '').strip().upper()
        answers_json[str(q.id)] = selected
        
        if selected == q.correct_option.upper():
            correct_count += 1
            
    # Calculate score out of 100
    score = int((correct_count / total_questions) * 100)
    
    # Create the submission record
    ExamSubmission.objects.create(
        user=request.user,
        exam=exam,
        answers_json=answers_json,
        score=score,
        completed_at=timezone.now()
    )
    
    # Reward XP (+200 XP)
    xp_reward = 200
    profile = request.user.profile
    profile.xp += xp_reward
    level_up = False
    
    while profile.xp >= profile.xp_to_next_level:
        profile.xp -= profile.xp_to_next_level
        profile.level += 1
        level_up = True
        
    profile.save()
    
    # Log activity
    UserActivity.objects.create(
        user=request.user,
        activity_type=UserActivity.ActivityType.LESSON_COMPLETE,
        metadata={
            'exam': exam.title,
            'score': score,
            'xp': xp_reward
        }
    )
    
    is_arabic = request.COOKIES.get('nexus_lang') == 'ar'
    Notification.objects.create(
        user=request.user,
        title='شهادة مكتملة / Exam Certified' if is_arabic else 'Exam Certified',
        message=f'لقد أكملت اختبار {exam.title} بنجاح وحصلت على {score}%!' if is_arabic else f'Successfully completed {exam.title} with a score of {score}%!',
        notification_type=Notification.NotificationType.SUCCESS,
        link='/dashboard/exams/'
    )
    
    return JsonResponse({
        'success': True,
        'score': score,
        'correct_count': correct_count,
        'total_questions': total_questions,
        'xp': profile.xp,
        'level': profile.level,
        'level_up': level_up,
        'xp_reward': xp_reward
    })


@login_required
def switch_role(request):
    courses = Course.objects.all().order_by('title')
    
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'instructor':
            course_id = request.POST.get('course_id')
            if not course_id:
                messages.error(request, 'Please select the course you teach.')
                return redirect('dashboard:switch_role')
            
            request.session['role'] = 'instructor'
            request.session['instructor_course_id'] = course_id
            messages.success(request, 'Successfully switched to Instructor Mode!')
            return redirect(f'/courses/manage/?course_id={course_id}')
        else:
            request.session['role'] = 'student'
            request.session.pop('instructor_course_id', None)
            messages.success(request, 'Successfully switched to Student Mode!')
            return redirect('/dashboard/')
            
    current_role = request.session.get('role', 'student')
    current_course_id = request.session.get('instructor_course_id')
    
    return render(request, 'dashboard/role_switch.html', {
        'courses': courses,
        'current_role': current_role,
        'current_course_id': current_course_id,
    })
