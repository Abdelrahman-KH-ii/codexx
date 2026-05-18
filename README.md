# DevFlow.io — AI Coding Education Platform

Futuristic AI-powered coding education platform built with **Django**, **PostgreSQL**, and **Django Templates**. React is used only for interactive widgets embedded inside server-rendered pages — no separate frontend build.

## Tech Stack

- Django 4.2+
- PostgreSQL (SQLite supported for quick local dev)
- HTML / CSS / JavaScript
- React 18 (CDN, embedded widgets)
- GSAP animations

## Project Structure

```
osama/
├── nexus/              # Project settings & URLs
├── accounts/           # Auth & user profiles
├── dashboard/          # Home & dashboard
├── courses/            # Courses, lessons, enrollments
├── ai_assistant/       # AI chat assistant
├── analytics/          # Progress & activity tracking
├── notifications/      # User notifications
├── templates/          # Django templates
│   ├── base.html
│   ├── base_hero.html  # 70/30 hero layout
│   ├── base_dashboard.html
│   └── components/
├── static/
│   ├── css/
│   └── js/react/       # React widgets (no build step)
└── manage.py
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
copy .env.example .env
```

For **PostgreSQL** (recommended):

```env
DB_ENGINE=postgresql
DB_NAME=nexus_edu
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Create the database:

```sql
CREATE DATABASE nexus_edu;
```

For quick local dev without PostgreSQL, use `DB_ENGINE=sqlite` in `.env`.

### 3. Migrate & seed

```bash
python manage.py migrate
python manage.py seed_data --demo-user
```

### 4. Run server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**

## Design system (Stitch)

UI is based on the **Cyber-Modern IDE** design exported from Google Stitch (`stitch_.zip`):

- Tokens: `static/css/variables.css`
- Components: `static/css/stitch-components.css`
- Full spec: `docs/DESIGN.md`

Screens mapped from Stitch:

| Stitch export | Django template |
|---------------|-----------------|
| `devflow/` | Home hero (`pages/home.html`) |
| `_1/` | Dashboard sidebar |
| `_2/` | Lesson IDE / playground |
| `full_stack/` | Course detail styling |

**Demo account:** `demo@nexus.ai` / `demo1234`

## Features

- Cinematic 70/30 hero layout (animated space + glass panel)
- User registration & authentication (email-based)
- AI-powered courses with modules & lessons
- Interactive coding playground (React widget)
- AI coding assistant chat (React widget)
- Dashboard with progress rings (React widget)
- Analytics charts (React widget)
- Notifications & XP/level system

## Architecture

- **Server-side rendering** via Django templates
- **React islands** mounted on `div.react-mount` elements
- **No Vite / Next.js** — everything runs from `python manage.py runserver`
- Modular Django apps with reusable template components

## Production

- Set `DEBUG=False` and a strong `SECRET_KEY`
- Use PostgreSQL with `DB_ENGINE=postgresql`
- Run `python manage.py collectstatic`
- Configure your WSGI server (gunicorn, etc.)

## Admin

```bash
python manage.py createsuperuser
```

Admin panel: **http://127.0.0.1:8000/admin/**
