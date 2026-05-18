from django.contrib import admin

from .models import FeaturedTip


@admin.register(FeaturedTip)
class FeaturedTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
