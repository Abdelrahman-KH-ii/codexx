from django.db import models


class FeaturedTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    icon = models.CharField(max_length=50, default='💡')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
