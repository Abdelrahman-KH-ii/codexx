"""Seed 30 courses across Gen AI, ML, NLP, Backend, Frontend, Flutter, Data Science, Analytics, DevOps."""

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from courses.models import Course, Lesson, Module

DEFAULT_LESSONS = [
    ('Introduction & Overview', 'intro', 'reading',
     'Welcome to this course! In this introductory lesson, we will cover the core objectives of this course, lay out the pathway to success, and introduce you to the key tools and environments you will be utilizing throughout your learning journey.\n\nBy the end of this lesson, you will have a solid conceptual understanding of the technology stack and be fully prepared to write your first line of code.', '', 15, 50),
    ('Hands-on Practice', 'practice', 'coding',
     'Now that we have covered the core concepts, it is time to put your knowledge to the test! Complete the coding exercise below by following the instructions carefully.\n\nYour goal is to implement the starter function, ensuring it passes all unit test assertions. Check your variables and logical branches before submitting.',
     '# Write your solution here\n\ndef run_exercise():\n    pass\n', 25, 75),
]


def course(slug, title, category, stack, difficulty, hours, price, student_count, short, desc, order):
    return {
        'slug': slug,
        'title': title,
        'category': category,
        'stack': stack,
        'difficulty': difficulty,
        'duration_hours': hours,
        'price': price,
        'student_count': student_count,
        'short_description': short,
        'description': desc,
        'order': order,
    }


COURSES_30 = [
    # Generative AI (4)
    course(
        'intro-generative-ai',
        'Introduction to Generative AI',
        'gen_ai',
        'general',
        'beginner',
        12,
        49.99,
        1850,
        'LLMs, diffusion models, and the Gen AI landscape.',
        'Embark on a transformative journey into the world of Generative AI. This course is specifically designed to demystify Large Language Models (LLMs), diffusion models, and the rapidly growing Gen AI ecosystem.\n\nWhat you will learn:\n• The architectural foundations of transformers and self-attention mechanisms.\n• How text generation models (GPT, Claude) and image generation models (Stable Diffusion, Midjourney) function behind the scenes.\n• Practical applications of generative AI across industries.\n• Responsible AI practices, ethics, and future technology trends.',
        1
    ),
    course(
        'prompt-engineering-mastery',
        'Prompt Engineering Mastery',
        'gen_ai',
        'general',
        'intermediate',
        16,
        59.99,
        2450,
        'Craft prompts that get reliable results from LLMs.',
        'Unlock the full potential of Large Language Models (LLMs) by mastering the art of prompt communication. This intermediate-level course equips you with advanced prompt engineering methodologies to build robust, predictable, and production-ready applications.\n\nKey Topics Covered:\n• Zero-shot, few-shot, and chain-of-thought prompting strategies.\n• System prompt architecture, XML formatting, and custom persona engineering.\n• Programmatic prompt evaluation, robustness testing, and prompt engineering tools.\n• Strategies to combat hallucinations, injection attacks, and LLM output bias.',
        2
    ),
    course(
        'llm-apis-integration',
        'LLM APIs & Integration',
        'gen_ai',
        'python',
        'intermediate',
        20,
        79.99,
        1250,
        'Connect OpenAI, Anthropic, and open models to your apps.',
        'Bridge the gap between raw AI capability and functional web software. In this comprehensive developer guide, you will learn to connect top-tier proprietary APIs (OpenAI, Anthropic) and open-source models (Llama, Mistral) directly to modern Python applications.\n\nCore Highlights:\n• Building secure API client pipelines, managing asynchronous streaming, and handle rate limits gracefully.\n• Generating and utilizing high-dimensional embeddings for semantic search workflows.\n• Advanced techniques for cost estimation, token usage monitoring, and latency optimization.\n• Crafting dynamic API wrappers and agentic pipelines.',
        3
    ),
    course(
        'rag-systems-building',
        'Building RAG Systems',
        'gen_ai',
        'python',
        'advanced',
        24,
        99.99,
        820,
        'Retrieval-augmented generation for enterprise knowledge.',
        'Take LLMs from general knowledge engines to specialized assistants with Retrieval-Augmented Generation (RAG). This advanced, code-intensive course details how to design, evaluate, and scale RAG systems using corporate documentation and knowledge bases.\n\nKey Focus Areas:\n• Document processing strategies: text extraction, optimal chunking, and overlap management.\n• Setting up and scaling vector databases (Pinecone, Chroma, pgvector).\n• Advanced retrieval techniques: hybrid keyword-vector search, re-ranking, and context compression.\n• Evaluating RAG pipelines for faithfulness, relevance, and semantic correctness.',
        4
    ),

    # Machine Learning (4)
    course(
        'ml-foundations-python',
        'ML Foundations with Python',
        'machine_learning',
        'python',
        'beginner',
        28,
        69.99,
        3400,
        'Scikit-learn, train/test splits, and model evaluation.',
        'Lay down the mathematical and programmatic foundations of modern machine learning. Using Python, scikit-learn, and pandas, you will learn how to go from raw data collections to functional predictive models.\n\nCourse Modules:\n• Practical data preprocessing: handling missing values, encoding categoricals, and feature scaling.\n• Understanding regression vs classification workflows and choosing the right objective function.\n• Standard validation routines: cross-validation, train-test splits, and stratified sampling.\n• Measuring performance with confusion matrices, ROC-AUC, and precision-recall metrics.',
        5
    ),
    course(
        'supervised-learning-deep',
        'Supervised Learning Deep Dive',
        'machine_learning',
        'python',
        'intermediate',
        22,
        89.99,
        1950,
        'Regression, classification, and ensemble methods.',
        'Take your machine learning expertise to the next level by exploring high-performance supervised learning algorithms. This course bridges mathematical theory and practical application to help you master predictive modeling.\n\nCourse Features:\n• Advanced linear and logistic regression models with L1/L2 regularization (Ridge, Lasso).\n• Non-linear models: decision trees, support vector machines (SVMs), and Naive Bayes.\n• Ensemble learning methods: Random Forests, AdaBoost, Gradient Boosting, and XGBoost.\n• Comprehensive hyperparameter tuning using Grid Search, Random Search, and Bayesian Optimization.',
        6
    ),
    course(
        'unsupervised-learning',
        'Unsupervised Learning & Clustering',
        'machine_learning',
        'python',
        'intermediate',
        18,
        59.99,
        1100,
        'PCA, K-means, and anomaly detection.',
        'Discover the hidden structures in unlabeled datasets. This course guides you through unsupervised learning techniques, dimensionality reduction, and sophisticated clustering methods designed to extract business value from unorganized data.\n\nWhat You Will Learn:\n• Dimensionality reduction algorithms like Principal Component Analysis (PCA) and t-SNE.\n• Hard and soft clustering approaches (K-Means, DBSCAN, Hierarchical, Gaussian Mixture Models).\n• Setting up anomaly detection workflows for fraud detection and system telemetry monitoring.\n• Building custom recommender pipelines using matrix factorization and collaborative filtering.',
        7
    ),
    course(
        'deep-learning-tensorflow',
        'Deep Learning with TensorFlow',
        'machine_learning',
        'python',
        'advanced',
        32,
        119.99,
        950,
        'Neural networks, CNNs, and training at scale.',
        'Dive into the architecture of deep neural networks. Leveraging Google\'s TensorFlow and Keras, you will learn to build, compile, and train massive deep learning models optimized for computer vision, sequence analysis, and generative tasks.\n\nCore Highlights:\n• Multilayer Perceptrons (MLPs): dense layers, backpropagation, and custom loss formulations.\n• Convolutional Neural Networks (CNNs) for image classification and feature maps optimization.\n• Recurrent Neural Networks (RNNs), LSTMs, and GRUs for temporal sequence modeling.\n• Production-ready training strategies: learning rate schedules, early stopping, and GPU scaling.',
        8
    ),

    # NLP (4)
    course(
        'nlp-fundamentals',
        'NLP Fundamentals',
        'nlp',
        'python',
        'beginner',
        20,
        49.99,
        1600,
        'Tokenization, embeddings, and text pipelines.',
        'Unlock the power of Natural Language Processing. This course provides an accessible introduction to the core techniques of processing human speech and text, converting raw strings into structured mathematical inputs.\n\nTopics Covered:\n• Text cleaning, regex pipelines, tokenization, lemmatization, and stop-word filtering.\n• Vectorization basics: Bag-of-Words, TF-IDF, and lexical statistics.\n• Word representation frameworks: Word2Vec, GloVe, and fastText embeddings.\n• Core syntax parsing, part-of-speech (POS) tagging, and Named Entity Recognition (NER).',
        9
    ),
    course(
        'text-classification-sentiment',
        'Text Classification & Sentiment',
        'nlp',
        'python',
        'intermediate',
        16,
        69.99,
        1340,
        'Build classifiers for reviews, tickets, and social data.',
        'Master the art of organizing text at scale. Learn to implement automated systems that classify support tickets, moderate online forums, and analyze sentiment across millions of customer reviews.\n\nCore Highlights:\n• Implementing baseline classifiers with Naive Bayes, Support Vector Machines, and Logistic Regression.\n• Moving to deep models: using 1D CNNs and LSTMs for text sequence classification.\n• Training multi-class and multi-label classifiers, and managing highly imbalanced classes.\n• Evaluating sentiment metrics and deploying text pipelines to production endpoints.',
        10
    ),
    course(
        'transformers-bert',
        'Transformers & BERT',
        'nlp',
        'python',
        'advanced',
        26,
        99.99,
        780,
        'Attention, Hugging Face, and fine-tuning transformers.',
        'Step into the cutting edge of NLP with transformer models. Learn how the self-attention mechanism revolutionized the AI landscape and discover how to fine-tune pre-trained models for state-of-the-art results.\n\nKey Concepts:\n• Transformer architecture: encoders, decoders, self-attention, and positional encoding.\n• The Hugging Face ecosystem: transformers library, tokenizers, and datasets.\n• Fine-tuning BERT, RoBERTa, and DeBERTa for custom sequence classification and QA tasks.\n• Optimization techniques: mixed-precision training, parameter-efficient fine-tuning (PEFT), and LoRA.',
        11
    ),
    course(
        'chatbots-nlp',
        'Building Chatbots with NLP',
        'nlp',
        'python',
        'intermediate',
        20,
        79.99,
        1420,
        'Intent detection, dialog flows, and LLM-powered bots.',
        'Design and deploy intelligent conversational systems that capture users\' intent and provide coherent, structured responses. This course covers everything from classic intent-based architectures to modern hybrid LLM dialog systems.\n\nCore Topics:\n• Building conversational logic using state machines and custom dialog flows.\n• Intent classification, entity extraction, and slot-filling with frameworks like Rasa.\n• Integrating LLM APIs into chat flows to handle unstructured conversational branches.\n• Designing memory adapters, session management, and chatbot UI layouts.',
        12
    ),

    # Backend — Django (3)
    course(
        'django-fundamentals',
        'Django Fundamentals',
        'backend',
        'django',
        'beginner',
        24,
        59.99,
        2900,
        'Models, views, templates, and the Django way.',
        'Master the web framework for perfectionists with deadlines. This course guides you from absolute beginner to building production-grade web applications utilizing Django\'s batteries-included architecture.\n\nKey Core Competencies:\n• Setting up the Django ORM: defining database tables, relationships, and queries.\n• Creating dynamic web interfaces with Class-Based Views (CBVs) and Django Templates.\n• Implementing the robust built-in authentication system, session control, and user profiles.\n• Mastering administrative customizations, forms validation, and CSRF protection.',
        13
    ),
    course(
        'django-rest-framework',
        'Django REST Framework',
        'backend',
        'django',
        'intermediate',
        22,
        79.99,
        2100,
        'REST APIs, serializers, and authentication.',
        'Turn your Django applications into backend engines for single-page applications and mobile backends. This course walks you through Django REST Framework (DRF) to design robust, standardized RESTful APIs.\n\nWhat You Will Learn:\n• Serializers: transforming complex DB model queries to JSON and validating incoming requests.\n• Implementing dynamic ViewSets and API routing for CRUD resources.\n• API security mechanisms: Token authentication, JWT authentication, and custom permissions.\n• Optimizing responses: pagination, throttling, and custom query filters.',
        14
    ),
    course(
        'django-production-apps',
        'Django Production Apps',
        'backend',
        'django',
        'advanced',
        28,
        99.99,
        1150,
        'Deploy, cache, Celery, and security hardening.',
        'Hardening Django for production scaling. This course focuses on complex backend topics like caching, background workers, security reviews, and devops practices needed to run high-traffic applications.\n\nKey Focus Areas:\n• Setting up Celery and Redis to handle heavy asynchronous background tasks.\n• Caching strategies: memcached/Redis integrations, template fragments caching, and low-level caching.\n• Hardening Django security: SSL redirects, secure cookies, and vulnerability scanning.\n• Database optimizations: connection pooling, select_related/prefetch_related tuning, and indexes.',
        15
    ),

    # Backend — Node.js (3)
    course(
        'nodejs-fundamentals',
        'Node.js Fundamentals',
        'backend',
        'nodejs',
        'beginner',
        20,
        49.99,
        3200,
        'JavaScript on the server: modules, async, npm.',
        'Unleash JavaScript on the server. In this beginner-friendly Backend course, you will learn the fundamentals of Node.js, the event loop, and modular JavaScript architecture.\n\nCourse Modules:\n• Demystifying the asynchronous event-driven loop and the non-blocking I/O model.\n• Utilizing Core Node.js Modules: Filesystem (fs), Path, HTTP, and Streams.\n• Working with npm: installing packages, managing dependencies, and semantic versioning.\n• Building baseline TCP and HTTP web servers completely from scratch.',
        16
    ),
    course(
        'express-rest-apis',
        'Express.js REST APIs',
        'backend',
        'nodejs',
        'intermediate',
        22,
        69.99,
        2500,
        'Routing, middleware, and MongoDB/PostgreSQL.',
        'Learn the standard minimalist framework for Node.js. In this course, you will build fast, scalable, and extremely robust RESTful APIs using Express.js and both SQL and NoSQL databases.\n\nKey Concepts Covered:\n• Express.js middleware paradigm: request parsing, logging, error handling, and security.\n• Designing highly structured API routing files, controllers, and validation.\n• Database integration: Mongoose for MongoDB, and Sequelize or pg-pool for PostgreSQL.\n• Securing endpoints with JWT, encrypting passwords with bcrypt, and handling CORS.',
        17
    ),
    course(
        'nodejs-microservices',
        'Node.js Microservices',
        'backend',
        'nodejs',
        'advanced',
        26,
        89.99,
        1200,
        'Services, message queues, and API gateways.',
        'Deconstruct monolithic backends into distributed microservice architectures. This advanced engineering course focuses on architectural design patterns, messaging brokers, and service communication.\n\nWhat You Will Learn:\n• Splitting monoliths into domain-driven microservices using Node.js and Express.\n• Event-driven communications using RabbitMQ, Kafka, or Redis Pub/Sub.\n• Implementing API Gateways for routing, rate limiting, and centralized authentication.\n• Monitoring distributed networks: distributed tracing, logs aggregation, and health checks.',
        18
    ),

    # Frontend — React (2)
    course(
        'react-complete-guide',
        'React Complete Guide',
        'frontend',
        'react',
        'beginner',
        30,
        59.99,
        4800,
        'Components, hooks, state, and modern React patterns.',
        'Master the world\'s most popular user interface library. Built for the modern web, this course takes you from basic HTML elements to single-page applications utilizing React 18.\n\nKey Core Competencies:\n• JSX Syntax, Component-Based UI architecture, and advanced Props distribution.\n• Core React Hooks: useState, useEffect, useRef, useMemo, and useCallback.\n• Global State Management: Context API, Redux Toolkit, or Zustand.\n• Client-side routing with React Router, forms validation, and responsive styled UI modules.',
        19
    ),
    course(
        'react-django-fullstack',
        'React + Django Full Stack',
        'frontend',
        'react',
        'intermediate',
        24,
        89.99,
        2200,
        'Connect React widgets to Django templates and APIs.',
        'Bridge the gap between frontend dynamism and backend stability. This course details the Islands Architecture, mounting reactive React widgets directly inside Django-rendered templates.\n\nCourse Focus:\n• Mounting React components to static DOM nodes, and exchanging data via dataset attributes.\n• Designing secure Django API endpoints consuming React requests with csrf tokens.\n• Bundling React widgets and consuming them cleanly inside Django static files.\n• End-to-end full-stack state coordination and modern deployment strategies.',
        20
    ),

    # Frontend — Vue (2)
    course(
        'vuejs-fundamentals',
        'Vue.js Fundamentals',
        'frontend',
        'vue',
        'beginner',
        22,
        49.99,
        2100,
        'Composition API, reactivity, and single-file components.',
        'Explore the progressive JavaScript framework. Known for its clean design and low learning curve, this course covers modern Vue 3 using the high-performance Composition API.\n\nKey Concepts:\n• Reactivity systems in Vue: ref, reactive, computed properties, and watch triggers.\n• Building clean, reusable Single File Components (SFCs) with setup syntax.\n• Directives (v-if, v-for, v-model) and parent-child component communication.\n• Setting up centralized store management with Pinia, and routing with Vue Router.',
        21
    ),
    course(
        'vue-node-fullstack',
        'Vue + Node.js Full Stack',
        'frontend',
        'vue',
        'intermediate',
        24,
        79.99,
        1350,
        'SPA with Vue frontend and Express backend.',
        'Build and deploy a unified Full Stack Single Page Application (SPA). This developer guide details how to coordinate a reactive Vue frontend with an Express.js backend engine.\n\nHighlights Include:\n• Setting up asynchronous API client networks using Axios with global interceptors.\n• Constructing robust JWT-based authorization pipelines spanning Vue state and Express cookies.\n• Coordinating database validation errors seamlessly to frontend components.\n• Bundling and hosting Vue production files on modern cloud networks.',
        22
    ),

    # Flutter (3)
    course(
        'flutter-basics',
        'Flutter Basics',
        'flutter',
        'flutter',
        'beginner',
        24,
        59.99,
        2800,
        'Widgets, layout, and your first mobile app.',
        'Build native cross-platform mobile apps using a single codebase. Leveraging Google\'s Flutter SDK and Dart, you will build and launch beautiful, fast apps for iOS and Android.\n\nWhat You Will Learn:\n• Mastering Dart: variables, OOP principles, asynchronous futures, and collection types.\n• Designing flexible layouts with Stateless and Stateful widgets.\n• Handling user interactions, inputs, forms validation, and loading indicators.\n• Working with custom assets, device fonts, and navigation routing.',
        23
    ),
    course(
        'flutter-state-management',
        'Flutter State Management',
        'flutter',
        'flutter',
        'intermediate',
        20,
        79.99,
        1600,
        'Provider, Riverpod, and scalable app architecture.',
        'Scale Flutter apps efficiently without spaghetti code. This course dives into professional application architectures and advanced state management techniques in Flutter.\n\nCourse Focus:\n• Understanding the reactive widget lifecycle and app state vs ephemeral state.\n• Detailed review of state management tools: Provider, ChangeNotifier, and Riverpod.\n• Implementing clean, modular architectures (MVVM, Clean Architecture) in Flutter.\n• Automated unit and widget testing for state pipelines and business logic.',
        24
    ),
    course(
        'flutter-firebase',
        'Flutter & Firebase',
        'flutter',
        'flutter',
        'intermediate',
        22,
        89.99,
        1850,
        'Auth, Firestore, and push notifications.',
        'Turn your Flutter app into a functional real-time platform. Connect your mobile applications directly to Google\'s Firebase suite to handle databases, assets, and notifications.\n\nCore Integration Targets:\n• Implementing User Sign-up, Login, and Social Authentication via Firebase Auth.\n• Storing and synchronizing application documents in real-time with Cloud Firestore.\n• Uploading mobile media files (images, audios) securely to Firebase Storage.\n• Dispatching push notifications with Firebase Cloud Messaging (FCM).',
        25
    ),

    # Data Science (3)
    course(
        'python-data-science',
        'Python for Data Science',
        'data_science',
        'python',
        'beginner',
        26,
        59.99,
        3900,
        'Jupyter, data wrangling, and exploratory analysis.',
        'Step into the world of Data Science. In this course, you will learn how to analyze massive datasets, perform exploratory research, and clean complex real-world data.\n\nCourse Modules:\n• Setting up modern data environments: Jupyter Notebooks, Anaconda, and VS Code.\n• Importing, parsing, and cleaning data from disparate formats (CSV, JSON, Excel, SQL).\n• Exploratory Data Analysis (EDA): identifying core correlations and data cleaning.\n• Lays the conceptual foundations for statistical algorithms and model fitting.',
        26
    ),
    course(
        'pandas-numpy-mastery',
        'Pandas & NumPy Mastery',
        'data_science',
        'python',
        'intermediate',
        22,
        79.99,
        2300,
        'Vectorized operations and DataFrame power tools.',
        'Speed up your data pipelines and master data frames. This developer guide explores high-performance data manipulation utilizing Python\'s NumPy and Pandas libraries.\n\nKey Concepts Covered:\n• Working with multi-dimensional NumPy arrays and utilizing high-speed vectorized arithmetic.\n• Advanced Pandas operations: multi-indexing, groupby aggregations, and merging dataframes.\n• Cleaning timeseries data, managing intervals, and optimizing memory usage.\n• Scaling data transformations to handle millions of records cleanly.',
        27
    ),
    course(
        'data-visualization',
        'Data Visualization',
        'data_science',
        'python',
        'intermediate',
        18,
        49.99,
        1700,
        'Matplotlib, Seaborn, and storytelling with charts.',
        'Make data speak. In this course, you will learn to turn complex statistics and raw numbers into stunning, interactive visual charts that communicate clear business insights.\n\nWhat You Will Learn:\n• Designing high-quality static charts using Matplotlib and Seaborn.\n• Creating dynamic, interactive web-ready plots using libraries like Plotly.\n• Choosing the right visual structure: scatter plots, heatmaps, box plots, and histograms.\n• Applying human design aesthetics, contrast, and color palettes to charts.',
        28
    ),

    # Data Analytics (1) + DevOps (1) = 30 total
    course(
        'sql-data-analytics',
        'SQL for Data Analytics',
        'data_analytics',
        'general',
        'beginner',
        20,
        39.99,
        4500,
        'Queries, joins, window functions, and reporting.',
        'Query data like a professional analyst. In this course, you will learn to write high-performance SQL queries to extract data, build business reports, and perform data transformations.\n\nTopics Covered:\n• Fundamentals of relational databases, SELECT statements, and advanced WHERE filtering.\n• Connecting tables securely using INNER JOIN, LEFT/RIGHT JOIN, and FULL OUTER JOIN.\n• Advanced analytics operations: GROUP BY, aggregation functions, and subqueries.\n• Mastery of Window Functions, Common Table Expressions (CTEs), and query optimizations.',
        29
    ),
    course(
        'devops-docker-k8s-cicd',
        'DevOps: Docker, Kubernetes & CI/CD',
        'devops',
        'general',
        'intermediate',
        30,
        99.99,
        3100,
        'Containers, orchestration, and automated pipelines.',
        'Bridge the gap between development and production. This practical engineering guide covers modern containerization, cluster orchestration, and automated CI/CD deployment pipelines.\n\nCourse Modules:\n• Writing robust Dockerfiles, managing container volumes, and linking services with Compose.\n• Standard cluster deployments using Kubernetes: Pods, Services, and Deployments.\n• Automating build and test suites using GitHub Actions and GitLab CI/CD pipelines.\n• Implementing Infrastructure as Code (IaC) principles to secure cloud environments.',
        30
    ),
]


class Command(BaseCommand):
    help = 'Seed 30 highly detailed courses with realistic prices and student counts across multiple categories'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Delete all courses before seeding')

    def handle(self, *args, **options):
        if options['clear']:
            count = Course.objects.count()
            Course.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing courses.'))

        created = 0
        updated = 0
        for data in COURSES_30:
            obj, was_created = Course.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    **data,
                    'is_published': True,
                    'is_ai_powered': True,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

            module, _ = Module.objects.update_or_create(
                course=obj,
                order=0,
                defaults={'title': f'Getting Started — {obj.title[:40]}'},
            )
            for les_order, (title, les_slug, ltype, content, starter, dur, xp) in enumerate(DEFAULT_LESSONS):
                Lesson.objects.update_or_create(
                    module=module,
                    slug=les_slug,
                    defaults={
                        'title': title,
                        'content': content,
                        'lesson_type': ltype,
                        'code_starter': starter,
                        'duration_minutes': dur,
                        'order': les_order,
                        'xp_reward': xp,
                    },
                )

        self.stdout.write(self.style.SUCCESS(
            f'Done: {created} created, {updated} updated — {Course.objects.count()} courses total.'
        ))
