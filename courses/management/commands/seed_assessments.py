import sys
from django.core.management.base import BaseCommand
from django.utils import timezone
from courses.models import Course, Assignment, Exam, ExamQuestion

class Command(BaseCommand):
    help = 'Seed Assignments and TIMED MCQ Exams'

    def handle(self, *args, **options):
        self.stdout.write("Seeding assignments and timed exams...")

        # 1. Fetch courses or fallback to existing
        courses = Course.objects.all()
        if not courses.exists():
            self.stdout.write(self.style.ERROR("No courses found. Please run seed_30_courses first!"))
            return

        c1 = Course.objects.filter(slug='intro-generative-ai').first() or courses[0]
        c2 = Course.objects.filter(slug='prompt-engineering-mastery').first() or (courses[1] if courses.count() > 1 else courses[0])

        # 2. Seed Assignments
        a1, created = Assignment.objects.update_or_create(
            course=c1,
            title="Algorithm Challenge: Fibonacci Series Generator",
            defaults={
                "description": (
                    "Write a Python function named `fibonacci(n)` that returns a list containing the "
                    "first `n` Fibonacci numbers.\n\n"
                    "### Requirements:\n"
                    "- Input: `n` (positive integer)\n"
                    "- Output: List of integers\n"
                    "- Example: `fibonacci(5)` should return `[0, 1, 1, 2, 3]`\n\n"
                    "Test your code in the Playground Editor and submit it directly to this assignment!"
                ),
                "points": 100,
                "due_date": timezone.now() + timezone.timedelta(days=5),
            }
        )
        self.stdout.write(f"Seeded Assignment: {a1.title} ({'Created' if created else 'Updated'})")

        a2, created = Assignment.objects.update_or_create(
            course=c2,
            title="Frontend Coding: Build a Beautiful Profile Component",
            defaults={
                "description": (
                    "Using pure HTML, CSS, and modern typography, build a highly polished personal profile card component "
                    "with rounded avatars, micro-interactions, HSL background color palettes, and glassmorphic shadows.\n\n"
                    "Submit your HTML/CSS file or copy-paste your code directly in the Universal Code Editor."
                ),
                "points": 150,
                "due_date": timezone.now() + timezone.timedelta(days=10),
            }
        )
        self.stdout.write(f"Seeded Assignment: {a2.title} ({'Created' if created else 'Updated'})")

        # 3. Seed Timed MCQ Exams
        exam1, created = Exam.objects.update_or_create(
            course=c1,
            title="Generative AI Fundamentals Certificate Exam",
            defaults={
                "duration_minutes": 20,
                "points": 100,
                "is_active": True,
            }
        )
        self.stdout.write(f"Seeded Exam: {exam1.title} ({'Created' if created else 'Updated'})")

        # Questions for Generative AI Exam
        questions1 = [
            {
                "question_text": "What does 'LLM' stand for in Generative AI?",
                "option_a": "Local Logistical Model",
                "option_b": "Large Language Model",
                "option_c": "Linear Layout Mapping",
                "option_d": "Linked Latent Matrix",
                "correct_option": "B"
            },
            {
                "question_text": "Which architecture is primarily responsible for modern LLM success and uses self-attention mechanisms?",
                "option_a": "Transformer Architecture",
                "option_b": "Recurrent Neural Network (RNN)",
                "option_c": "Convolutional Neural Network (CNN)",
                "option_d": "Multilayer Perceptron (MLP)",
                "correct_option": "A"
            },
            {
                "question_text": "What term describes when an AI model confidently generates incorrect or fabricated facts?",
                "option_a": "Stochastic Interpolation",
                "option_b": "Hallucination",
                "option_c": "Hyperparameter Tuning",
                "option_d": "Gradient Ascent",
                "correct_option": "B"
            },
            {
                "question_text": "Which type of generative model is commonly used to synthesize realistic images like Midjourney or Stable Diffusion?",
                "option_a": "Linear Classifiers",
                "option_b": "Decision Trees",
                "option_c": "Diffusion Models",
                "option_d": "Clustering Models",
                "correct_option": "C"
            },
            {
                "question_text": "What is the purpose of 'temperature' settings in generative model outputs?",
                "option_a": "Regulates the physical heat of the server GPU hosting the LLM",
                "option_b": "Determines the random creativity vs. logical deterministic nature of generated outputs",
                "option_c": "Calculates token processing latency",
                "option_d": "Sets constraints on token input counts",
                "correct_option": "B"
            }
        ]

        for i, q in enumerate(questions1):
            ExamQuestion.objects.update_or_create(
                exam=exam1,
                question_text=q["question_text"],
                defaults={
                    "option_a": q["option_a"],
                    "option_b": q["option_b"],
                    "option_c": q["option_c"],
                    "option_d": q["option_d"],
                    "correct_option": q["correct_option"],
                }
            )
        self.stdout.write("Seeded 5 questions for Generative AI Certificate Exam.")

        # Exam 2: Python Programming Core Certification
        exam2, created = Exam.objects.update_or_create(
            course=c2,
            title="Python Advanced Concepts & Patterns Certification",
            defaults={
                "duration_minutes": 15,
                "points": 100,
                "is_active": True,
            }
        )
        self.stdout.write(f"Seeded Exam: {exam2.title} ({'Created' if created else 'Updated'})")

        questions2 = [
            {
                "question_text": "Which keyword is used in Python to define a generator function that yields values lazily?",
                "option_a": "return",
                "option_b": "yield",
                "option_c": "generator",
                "option_d": "lazy",
                "correct_option": "B"
            },
            {
                "question_text": "What is the correct output of list comprehension expression: [x*2 for x in range(3)]?",
                "option_a": "[0, 2, 4]",
                "option_b": "[2, 4, 6]",
                "option_c": "[0, 1, 2]",
                "option_d": "[0, 2]",
                "correct_option": "A"
            },
            {
                "question_text": "Which Python decorator is used to define a class method that operates on the class object itself rather than instances?",
                "option_a": "@staticmethod",
                "option_b": "@classmethod",
                "option_c": "@property",
                "option_d": "@instanceoverride",
                "correct_option": "B"
            }
        ]

        for i, q in enumerate(questions2):
            ExamQuestion.objects.update_or_create(
                exam=exam2,
                question_text=q["question_text"],
                defaults={
                    "option_a": q["option_a"],
                    "option_b": q["option_b"],
                    "option_c": q["option_c"],
                    "option_d": q["option_d"],
                    "correct_option": q["correct_option"],
                }
            )
        self.stdout.write("Seeded 3 questions for Python advanced certification.")
        self.stdout.write(self.style.SUCCESS("All assessments seeded successfully!"))
