from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with email login support."""

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.email


class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    streak_days = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.email} — L{self.level}'

    @property
    def xp_to_next_level(self):
        return self.level * 500

    @property
    def xp_progress_percent(self):
        if self.xp_to_next_level == 0:
            return 100
        return min(100, int((self.xp % self.xp_to_next_level) / self.xp_to_next_level * 100))
