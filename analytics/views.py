from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone

from courses.models import Enrollment, LessonProgress

from .models import DailyStat, UserActivity


@login_required
def analytics_view(request):
    user = request.user
    today = timezone.now().date()
    week_ago = today - timedelta(days=6)

    daily_stats = DailyStat.objects.filter(user=user, date__gte=week_ago).order_by('date')
    activities = UserActivity.objects.filter(user=user)[:15]

    enrollments = Enrollment.objects.filter(user=user).select_related('course')
    completed_lessons = LessonProgress.objects.filter(user=user, completed=True).count()
    total_xp_week = daily_stats.aggregate(total=Sum('xp_earned'))['total'] or 0

    activity_breakdown = (
        UserActivity.objects.filter(user=user, created_at__date__gte=week_ago)
        .values('activity_type')
        .annotate(count=Count('id'))
    )

    chart_labels = []
    chart_minutes = []
    chart_lessons = []
    for i in range(7):
        d = week_ago + timedelta(days=i)
        chart_labels.append(d.strftime('%a'))
        stat = daily_stats.filter(date=d).first()
        chart_minutes.append(stat.minutes_studied if stat else 0)
        chart_lessons.append(stat.lessons_completed if stat else 0)

    return render(request, 'analytics/index.html', {
        'daily_stats': daily_stats,
        'activities': activities,
        'enrollments': enrollments,
        'completed_lessons': completed_lessons,
        'total_xp_week': total_xp_week,
        'activity_breakdown': activity_breakdown,
        'chart_labels': chart_labels,
        'chart_minutes': chart_minutes,
        'chart_lessons': chart_lessons,
        'profile': user.profile,
    })
