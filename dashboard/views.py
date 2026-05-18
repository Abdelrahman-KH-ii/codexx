from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView

from courses.models import Course, Enrollment, LessonProgress
from notifications.models import Notification

from .models import FeaturedTip


class HomeView(TemplateView):
    template_name = 'pages/home.html'

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
