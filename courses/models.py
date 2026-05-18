from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Course(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    class Category(models.TextChoices):
        GEN_AI = 'gen_ai', 'Generative AI'
        MACHINE_LEARNING = 'machine_learning', 'Machine Learning'
        NLP = 'nlp', 'NLP'
        BACKEND = 'backend', 'Backend'
        FRONTEND = 'frontend', 'Frontend'
        FLUTTER = 'flutter', 'Flutter'
        DATA_SCIENCE = 'data_science', 'Data Science'
        DATA_ANALYTICS = 'data_analytics', 'Data Analytics'
        DEVOPS = 'devops', 'DevOps'

    class Stack(models.TextChoices):
        GENERAL = 'general', 'General'
        DJANGO = 'django', 'Django'
        NODEJS = 'nodejs', 'Node.js'
        REACT = 'react', 'React'
        VUE = 'vue', 'Vue.js'
        FLUTTER = 'flutter', 'Flutter'
        PYTHON = 'python', 'Python'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)
    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.BACKEND,
    )
    stack = models.CharField(
        max_length=20,
        choices=Stack.choices,
        default=Stack.GENERAL,
        help_text='Tech stack track (e.g. Django vs Node.js for backend)',
    )
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.BEGINNER)
    duration_hours = models.PositiveIntegerField(default=10)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=29.99, help_text='Course enrollment price in USD')
    student_count = models.PositiveIntegerField(default=0, help_text='Baseline enrolled student count')
    is_published = models.BooleanField(default=True)
    is_ai_powered = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    @property
    def lesson_count(self):
        return Lesson.objects.filter(module__course=self).count()

    @property
    def total_students(self):
        return self.student_count + self.enrollments.count()

    @property
    def total_revenue(self):
        return self.price * self.total_students

    @property
    def category_label(self):
        return self.get_category_display()

    @property
    def stack_label(self):
        return self.get_stack_display()


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = [['course', 'order']]

    def __str__(self):
        return f'{self.course.title} — {self.title}'


class Lesson(models.Model):
    class LessonType(models.TextChoices):
        VIDEO = 'video', 'Video'
        READING = 'reading', 'Reading'
        CODING = 'coding', 'Coding Challenge'
        QUIZ = 'quiz', 'Quiz'

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    content = models.TextField()
    lesson_type = models.CharField(max_length=20, choices=LessonType.choices, default=LessonType.READING)
    code_starter = models.TextField(blank=True, help_text='Starter code for coding lessons')
    code_solution = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=15)
    order = models.PositiveIntegerField(default=0)
    xp_reward = models.PositiveIntegerField(default=50)

    class Meta:
        ordering = ['order']
        unique_together = [['module', 'slug']]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson', kwargs={
            'course_slug': self.module.course.slug,
            'lesson_slug': self.slug,
        })


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [['user', 'course']]

    def __str__(self):
        return f'{self.user.email} → {self.course.title}'

    @property
    def progress_percent(self):
        total = self.course.lesson_count
        if total == 0:
            return 0
        completed = LessonProgress.objects.filter(
            user=self.user,
            lesson__module__course=self.course,
            completed=True,
        ).count()
        return int(completed / total * 100)


class LessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    code_submitted = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [['user', 'lesson']]

    def __str__(self):
        status = '✓' if self.completed else '…'
        return f'{status} {self.user.email} — {self.lesson.title}'
