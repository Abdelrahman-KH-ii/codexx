from django.conf import settings
from django.db import models


class UserActivity(models.Model):
    class ActivityType(models.TextChoices):
        LOGIN = 'login', 'Login'
        LESSON_COMPLETE = 'lesson_complete', 'Lesson Complete'
        ENROLLMENT = 'enrollment', 'Enrollment'
        AI_CHAT = 'ai_chat', 'AI Chat'
        CODE_RUN = 'code_run', 'Code Run'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ActivityType.choices)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'user activities'

    def __str__(self):
        return f'{self.user.email} — {self.activity_type}'


class DailyStat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_stats')
    date = models.DateField()
    minutes_studied = models.PositiveIntegerField(default=0)
    lessons_completed = models.PositiveIntegerField(default=0)
    xp_earned = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [['user', 'date']]
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.email} — {self.date}'
