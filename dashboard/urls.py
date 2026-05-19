from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('assignments/', views.assignments_list_view, name='assignments'),
    path('exams/', views.exams_list_view, name='exams'),
    path('exams/<int:exam_id>/take/', views.take_exam_view, name='take_exam'),
    path('exams/<int:exam_id>/submit/', views.submit_exam_ajax, name='submit_exam'),
]
