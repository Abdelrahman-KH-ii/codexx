from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from courses.models import Course, Lesson, Module
from dashboard.models import FeaturedTip
from notifications.models import Notification

User = get_user_model()


COURSES = [
    {
        'title': 'Python AI Foundations',
        'slug': 'python-ai-foundations',
        'description': 'Master Python fundamentals with AI-guided exercises. From variables to machine learning prep.',
        'short_description': 'Build Python skills with an AI mentor at your side.',
        'difficulty': 'beginner',
        'duration_hours': 24,
        'modules': [
            {
                'title': 'Getting Started',
                'lessons': [
                    ('Hello, Python', 'hello-python', 'reading', 'Welcome to Python! Variables store data.\n\n```python\nname = "Nexus"\nprint(name)\n```', '', 10),
                    ('Your First Function', 'first-function', 'coding', 'Write a function that greets a user.', 'def greet(name):\n    return f"Hello, {name}!"\n', 20),
                ],
            },
            {
                'title': 'Data Structures',
                'lessons': [
                    ('Lists & Loops', 'lists-loops', 'reading', 'Lists hold collections. Loops iterate over them.', '', 15),
                    ('List Comprehensions', 'list-comprehensions', 'coding', 'Transform lists elegantly with comprehensions.', 'numbers = [1, 2, 3, 4, 5]\nsquares = []\n', 25),
                ],
            },
        ],
    },
    {
        'title': 'Full-Stack Django Mastery',
        'slug': 'django-mastery',
        'description': 'Build production web apps with Django, PostgreSQL, and modern frontend patterns.',
        'short_description': 'Server-rendered apps with embedded React widgets.',
        'difficulty': 'intermediate',
        'duration_hours': 32,
        'modules': [
            {
                'title': 'Django Core',
                'lessons': [
                    ('Models & ORM', 'models-orm', 'reading', 'Django ORM maps Python classes to database tables.', '', 20),
                    ('Views & Templates', 'views-templates', 'coding', 'Create a view that renders a template.', 'from django.shortcuts import render\n\ndef home(request):\n    pass\n', 30),
                ],
            },
        ],
    },
    {
        'title': 'React for Django Developers',
        'slug': 'react-django',
        'description': 'Embed interactive React widgets inside Django templates without a separate frontend build.',
        'short_description': 'Islands architecture for premium UIs.',
        'difficulty': 'advanced',
        'duration_hours': 18,
        'modules': [
            {
                'title': 'React Islands',
                'lessons': [
                    ('Embedding React', 'embedding-react', 'reading', 'Load React from CDN and mount components on DOM nodes.', '', 15),
                    ('Building a Widget', 'building-widget', 'coding', 'Create a counter component with React.createElement.', 'const { useState } = React;\n', 25),
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed demo courses, tips, and optional demo user'

    def add_arguments(self, parser):
        parser.add_argument('--demo-user', action='store_true', help='Create demo@nexus.ai user')

    def handle(self, *args, **options):
        for course_data in COURSES:
            modules_data = course_data.pop('modules')
            course, created = Course.objects.update_or_create(
                slug=course_data['slug'],
                defaults={**course_data, 'is_published': True, 'is_ai_powered': True},
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} course: {course.title}')

            for mod_order, mod_data in enumerate(modules_data):
                module, _ = Module.objects.update_or_create(
                    course=course,
                    order=mod_order,
                    defaults={'title': mod_data['title']},
                )
                for les_order, (title, slug, ltype, content, starter, duration) in enumerate(mod_data['lessons']):
                    Lesson.objects.update_or_create(
                        module=module,
                        slug=slug,
                        defaults={
                            'title': title,
                            'content': content,
                            'lesson_type': ltype,
                            'code_starter': starter,
                            'duration_minutes': duration,
                            'order': les_order,
                            'xp_reward': 50 + les_order * 10,
                        },
                    )

        tips = [
            ('Ship daily', 'Consistency beats intensity. Code 30 minutes every day.', '🚀'),
            ('Ask Nexus AI', 'Stuck on a bug? Your AI assistant is one click away.', '🤖'),
            ('Complete challenges', 'Coding lessons earn XP. Level up your profile.', '⚡'),
        ]
        for i, (title, content, icon) in enumerate(tips):
            FeaturedTip.objects.update_or_create(
                title=title,
                defaults={'content': content, 'icon': icon, 'order': i, 'is_active': True},
            )

        if options['demo_user']:
            user, created = User.objects.get_or_create(
                email='demo@nexus.ai',
                defaults={'username': 'demo'},
            )
            if created:
                user.set_password('demo1234')
                user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS('Demo user: demo@nexus.ai / demo1234 (staff admin)'))
            else:
                if not user.is_staff:
                    user.is_staff = True
                    user.save(update_fields=['is_staff'])
            Notification.objects.get_or_create(
                user=user,
                title='Welcome to Nexus AI',
                defaults={
                    'message': 'Explore courses and chat with your AI coding mentor.',
                    'notification_type': Notification.NotificationType.AI,
                    'link': '/courses/',
                },
            )

        self.stdout.write(self.style.SUCCESS('Seed complete.'))
