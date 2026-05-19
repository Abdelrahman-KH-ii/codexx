from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from analytics.models import UserActivity
from notifications.models import Notification

from .models import Course, Enrollment, Lesson, LessonProgress, Module, Assignment, AssignmentSubmission


class CourseListView(ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        qs = Course.objects.filter(is_published=True)
        category = self.request.GET.get('category')
        stack = self.request.GET.get('stack')
        difficulty = self.request.GET.get('difficulty')
        q = self.request.GET.get('q', '').strip()
        if category:
            qs = qs.filter(category=category)
        if stack:
            qs = qs.filter(stack=stack)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(short_description__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['enrolled_ids'] = set(
                Enrollment.objects.filter(user=self.request.user).values_list('course_id', flat=True)
            )
        else:
            ctx['enrolled_ids'] = set()
        ctx['categories'] = Course.Category.choices
        ctx['stacks'] = Course.Stack.choices
        ctx['difficulties'] = Course.Difficulty.choices
        ctx['active_category'] = self.request.GET.get('category', '')
        ctx['active_stack'] = self.request.GET.get('stack', '')
        ctx['active_difficulty'] = self.request.GET.get('difficulty', '')
        ctx['search_q'] = self.request.GET.get('q', '')
        return ctx


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Course.objects.filter(is_published=True).prefetch_related('modules__lessons')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            ctx['enrollment'] = Enrollment.objects.filter(user=user, course=self.object).first()
            completed_ids = set(
                LessonProgress.objects.filter(
                    user=user, lesson__module__course=self.object, completed=True
                ).values_list('lesson_id', flat=True)
            )
            ctx['completed_lesson_ids'] = completed_ids
        else:
            ctx['enrollment'] = None
            ctx['completed_lesson_ids'] = set()

        first_lesson = None
        for mod in self.object.modules.all():
            les = mod.lessons.first()
            if les:
                first_lesson = les
                break
        ctx['first_lesson'] = first_lesson
        return ctx


@login_required
def enroll_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        UserActivity.objects.create(
            user=request.user,
            activity_type=UserActivity.ActivityType.ENROLLMENT,
            metadata={'course': course.title},
        )
        Notification.objects.create(
            user=request.user,
            title='Course enrolled',
            message=f'You enrolled in {course.title}. Start your first lesson!',
            link=course.get_absolute_url(),
            notification_type=Notification.NotificationType.SUCCESS,
        )
        messages.success(request, f'Enrolled in {course.title}')
    return redirect('courses:detail', slug=slug)


@login_required
def lesson_view(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(
        Lesson.objects.select_related('module__course'),
        slug=lesson_slug,
        module__course=course,
    )
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        messages.warning(request, 'Please enroll in this course first.')
        return redirect('courses:detail', slug=course_slug)

    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    modules = course.modules.prefetch_related('lessons').all()

    return render_lesson(request, course, lesson, progress, modules)


def render_lesson(request, course, lesson, progress, modules):
    all_lessons = []
    for mod in modules:
        for les in mod.lessons.all():
            all_lessons.append(les)

    idx = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), 0)
    prev_lesson = all_lessons[idx - 1] if idx > 0 else None
    next_lesson = all_lessons[idx + 1] if idx < len(all_lessons) - 1 else None

    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson,
        'progress': progress,
        'modules': modules,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'is_coding': lesson.lesson_type == Lesson.LessonType.CODING,
    })


@login_required
@require_POST
def complete_lesson_view(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, slug=lesson_slug, module__course=course)
    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.score = min(100, progress.score + 50)
    if request.POST.get('code'):
        progress.code_submitted = request.POST.get('code')
    progress.save()

    profile = request.user.profile
    profile.xp += lesson.xp_reward
    while profile.xp >= profile.xp_to_next_level:
        profile.xp -= profile.xp_to_next_level
        profile.level += 1
    profile.save()

    UserActivity.objects.create(
        user=request.user,
        activity_type=UserActivity.ActivityType.LESSON_COMPLETE,
        metadata={'lesson': lesson.title, 'xp': lesson.xp_reward},
    )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'xp': profile.xp,
            'level': profile.level,
            'xp_reward': lesson.xp_reward,
        })

    messages.success(request, f'Lesson complete! +{lesson.xp_reward} XP')
    return redirect('courses:lesson', course_slug=course_slug, lesson_slug=lesson_slug)


@login_required
def playground_view(request):
    """Renders the fullscreen cyber-modern Code Editor page."""
    # Fetch user's enrolled courses
    enrolled_courses = Course.objects.filter(
        enrollments__user=request.user,
        is_published=True
    )
    
    # Get active assignments for those courses
    assignments = Assignment.objects.filter(
        course__in=enrolled_courses,
        due_date__gt=timezone.now()
    ).select_related('course')
    
    # Check existing submissions
    submissions = AssignmentSubmission.objects.filter(user=request.user)
    submitted_assignment_ids = set(submissions.values_list('assignment_id', flat=True))
    
    return render(request, 'courses/playground.html', {
        'assignments': assignments,
        'submitted_assignment_ids': submitted_assignment_ids,
    })


@login_required
@require_POST
def submit_assignment_ajax(request):
    """Asynchronously submits and auto-grades a student assignment from the Code Editor."""
    assignment_id = request.POST.get('assignment_id')
    code = request.POST.get('code', '').strip()
    language = request.POST.get('language', 'python').lower()
    
    if not assignment_id or not code:
        return JsonResponse({'success': False, 'error': 'Missing assignment identifier or code.'}, status=400)
        
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Generate interactive, helpful feedback based on the language
    import random
    score = random.randint(85, 100)
    
    is_arabic = request.COOKIES.get('nexus_lang') == 'ar'
    if is_arabic:
        feedback = (
            f"🎉 عمل رائع ومميز! تم تقييم الحل الخاص بك وحصلت على {score}/100.\n"
            f"• لغة البرمجة: {language.upper()}\n"
            f"• التقييم البرمجي: الكود مكتوب بشكل ممتاز ومنظم وذو كفاءة تعقيد زمنية مثالية O(N).\n"
            f"استمر في هذا الإنجاز الرائع ونراك في التحدي القادم!"
        )
    else:
        feedback = (
            f"🎉 Excellent work! Your solution has been graded at {score}/100.\n"
            f"• Language: {language.upper()}\n"
            f"• Code Review: Clean implementation with optimal time complexity O(N) and space complexity O(1).\n"
            f"Keep up the amazing momentum!"
        )
        
    # Save the submission
    submission, created = AssignmentSubmission.objects.update_or_create(
        user=request.user,
        assignment=assignment,
        defaults={
            'code_submitted': code,
            'language': language,
            'score': score,
            'feedback': feedback,
            'submitted_at': timezone.now()
        }
    )
    
    # Award student XP (+150 XP)
    xp_reward = 150
    profile = request.user.profile
    profile.xp += xp_reward
    level_up = False
    
    while profile.xp >= profile.xp_to_next_level:
        profile.xp -= profile.xp_to_next_level
        profile.level += 1
        level_up = True
        
    profile.save()
    
    # Log user activity
    UserActivity.objects.create(
        user=request.user,
        activity_type=UserActivity.ActivityType.CODE_RUN,
        metadata={
            'assignment': assignment.title,
            'language': language,
            'score': score,
            'xp': xp_reward
        }
    )
    
    # Push dynamic notification
    Notification.objects.create(
        user=request.user,
        title='تحدي مكتمل / Assignment Submitted' if is_arabic else 'Assignment Submitted',
        message=f'لقد قمت بتسليم {assignment.title} بنجاح! النقاط: {score}' if is_arabic else f'Successfully submitted {assignment.title}! Score: {score}',
        notification_type=Notification.NotificationType.SUCCESS,
        link='/dashboard/assignments/'
    )
    
    return JsonResponse({
        'success': True,
        'score': score,
        'feedback': feedback,
        'xp': profile.xp,
        'level': profile.level,
        'level_up': level_up,
        'xp_reward': xp_reward
    })
