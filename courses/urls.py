from django.urls import path

from . import admin_views, views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='list'),
    path('manage/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('manage/add/', admin_views.admin_course_create, name='admin_create'),
    path('manage/students/enroll/', admin_views.admin_enroll_student, name='admin_enroll_student'),
    path('manage/students/unenroll/<int:enrollment_id>/', admin_views.admin_unenroll_student, name='admin_unenroll_student'),
    path('manage/attendance/save/', admin_views.admin_attendance_save, name='admin_attendance_save'),
    path('manage/assignments/add/', admin_views.admin_assignment_add, name='admin_assignment_add'),
    path('manage/<slug:slug>/', admin_views.admin_course_manage, name='admin_manage'),
    path('manage/<slug:slug>/edit/', admin_views.admin_course_edit, name='admin_edit'),
    path('manage/<slug:slug>/delete/', admin_views.admin_course_delete, name='admin_delete'),
    path('manage/<slug:slug>/toggle-publish/', admin_views.admin_course_toggle_publish, name='admin_toggle_publish'),
    path('manage/<slug:slug>/modules/add/', admin_views.admin_module_add, name='admin_module_add'),
    path('manage/<slug:slug>/modules/<int:module_id>/lessons/add/', admin_views.admin_lesson_add, name='admin_lesson_add'),
    path('playground/', views.playground_view, name='playground'),
    path('assignments/submit/', views.submit_assignment_ajax, name='submit_assignment'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='detail'),
    path('<slug:slug>/enroll/', views.enroll_view, name='enroll'),
    path('<slug:course_slug>/lesson/<slug:lesson_slug>/', views.lesson_view, name='lesson'),
    path(
        '<slug:course_slug>/lesson/<slug:lesson_slug>/complete/',
        views.complete_lesson_view,
        name='complete_lesson',
    ),
]
