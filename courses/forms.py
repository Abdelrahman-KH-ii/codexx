from django import forms

from .models import Course, Lesson, Module


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'slug', 'short_description', 'description',
            'category', 'stack', 'difficulty', 'duration_hours',
            'price', 'student_count',
            'is_published', 'is_ai_powered', 'order', 'thumbnail',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'glass-input'}),
            'slug': forms.TextInput(attrs={'class': 'glass-input'}),
            'short_description': forms.TextInput(attrs={'class': 'glass-input'}),
            'description': forms.Textarea(attrs={'class': 'glass-input', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'glass-input'}),
            'stack': forms.Select(attrs={'class': 'glass-input'}),
            'difficulty': forms.Select(attrs={'class': 'glass-input'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'glass-input'}),
            'price': forms.NumberInput(attrs={'class': 'glass-input', 'step': '0.01'}),
            'student_count': forms.NumberInput(attrs={'class': 'glass-input'}),
            'order': forms.NumberInput(attrs={'class': 'glass-input'}),
            'thumbnail': forms.FileInput(attrs={'class': 'glass-input'}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'glass-input'}),
            'description': forms.Textarea(attrs={'class': 'glass-input', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'glass-input'}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'title', 'slug', 'content', 'lesson_type',
            'code_starter', 'code_solution',
            'duration_minutes', 'order', 'xp_reward',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'glass-input'}),
            'slug': forms.TextInput(attrs={'class': 'glass-input'}),
            'content': forms.Textarea(attrs={'class': 'glass-input', 'rows': 6}),
            'lesson_type': forms.Select(attrs={'class': 'glass-input'}),
            'code_starter': forms.Textarea(attrs={'class': 'glass-input', 'rows': 4}),
            'code_solution': forms.Textarea(attrs={'class': 'glass-input', 'rows': 4}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'glass-input'}),
            'order': forms.NumberInput(attrs={'class': 'glass-input'}),
            'xp_reward': forms.NumberInput(attrs={'class': 'glass-input'}),
        }
