from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CourseForm, LessonForm, ModuleForm
from .models import Course, Lesson, Module, Enrollment

User = get_user_model()


@staff_member_required
def admin_dashboard(request):
    courses = Course.objects.all().order_by('category', 'order')
    
    # Calculate premium stats
    total_simulated = sum(c.student_count for c in courses)
    total_real = Enrollment.objects.count()
    total_learners = total_simulated + total_real
    total_revenue = sum(c.total_revenue for c in courses)
    
    stats = {
        'total': courses.count(),
        'published': courses.filter(is_published=True).count(),
        'total_learners': total_learners,
        'total_revenue': total_revenue,
        'total_real': total_real,
        'by_category': {},
    }
    
    for cat, label in Course.Category.choices:
        stats['by_category'][label] = courses.filter(category=cat).count()
        
    # Get students registry
    students = User.objects.all().select_related('profile').prefetch_related('enrollments__course')
    
    student_q = request.GET.get('student_q', '').strip()
    if student_q:
        students = students.filter(email__icontains=student_q)
        
    return render(request, 'courses/admin/dashboard.html', {
        'courses': courses,
        'stats': stats,
        'students': students,
        'all_courses': Course.objects.filter(is_published=True).order_by('title'),
        'categories': Course.Category.choices,
        'stacks': Course.Stack.choices,
        'student_q': student_q,
    })


@staff_member_required
@require_POST
def admin_enroll_student(request):
    user_id = request.POST.get('user_id')
    course_id = request.POST.get('course_id')
    
    if not user_id or not course_id:
        messages.error(request, 'Select both a user and a course.')
        return redirect('courses:admin_dashboard')
        
    user = get_object_or_404(User, pk=user_id)
    course = get_object_or_404(Course, pk=course_id)
    
    enrollment, created = Enrollment.objects.get_or_create(user=user, course=course)
    if created:
        messages.success(request, f'Successfully enrolled {user.email} in "{course.title}".')
    else:
        messages.info(request, f'{user.email} is already enrolled in "{course.title}".')
        
    return redirect('courses:admin_dashboard')


@staff_member_required
@require_POST
def admin_unenroll_student(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    user_email = enrollment.user.email
    course_title = enrollment.course.title
    enrollment.delete()
    messages.success(request, f'Successfully unenrolled {user_email} from "{course_title}".')
    return redirect('courses:admin_dashboard')


@staff_member_required
def admin_course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            Module.objects.create(course=course, title='Module 1 — Introduction', order=0)
            messages.success(request, f'Course "{course.title}" created.')
            return redirect('courses:admin_manage', slug=course.slug)
    else:
        form = CourseForm()
    return render(request, 'courses/admin/course_form.html', {
        'form': form,
        'title': 'Add new course',
    })


@staff_member_required
def admin_course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated.')
            return redirect('courses:admin_manage', slug=course.slug)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/admin/course_form.html', {
        'form': form,
        'course': course,
        'title': f'Edit: {course.title}',
    })


@staff_member_required
def admin_course_manage(request, slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('modules__lessons'),
        slug=slug,
    )
    module_form = ModuleForm()
    lesson_form = LessonForm()
    return render(request, 'courses/admin/course_manage.html', {
        'course': course,
        'module_form': module_form,
        'lesson_form': lesson_form,
    })


@staff_member_required
@require_POST
def admin_module_add(request, slug):
    course = get_object_or_404(Course, slug=slug)
    form = ModuleForm(request.POST)
    if form.is_valid():
        module = form.save(commit=False)
        module.course = course
        module.save()
        messages.success(request, f'Module "{module.title}" added.')
    else:
        messages.error(request, 'Could not add module. Check the form.')
    return redirect('courses:admin_manage', slug=slug)


@staff_member_required
@require_POST
def admin_lesson_add(request, slug, module_id):
    course = get_object_or_404(Course, slug=slug)
    module = get_object_or_404(Module, pk=module_id, course=course)
    form = LessonForm(request.POST)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.module = module
        if not lesson.slug:
            from django.utils.text import slugify
            lesson.slug = slugify(lesson.title)
        lesson.save()
        messages.success(request, f'Lesson "{lesson.title}" added.')
    else:
        messages.error(request, 'Could not add lesson.')
    return redirect('courses:admin_manage', slug=slug)


@staff_member_required
@require_POST
def admin_course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug)
    title = course.title
    course.delete()
    messages.success(request, f'Course "{title}" deleted.')
    return redirect('courses:admin_dashboard')


@staff_member_required
@require_POST
def admin_course_toggle_publish(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course.is_published = not course.is_published
    course.save(update_fields=['is_published'])
    status = 'published' if course.is_published else 'unpublished'
    messages.success(request, f'Course {status}.')
    return redirect('courses:admin_dashboard')
