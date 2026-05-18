from django.contrib import admin

from .models import DailyStat, UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'created_at')
    list_filter = ('activity_type',)


@admin.register(DailyStat)
class DailyStatAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'minutes_studied', 'lessons_completed', 'xp_earned')
