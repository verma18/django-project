# MUSICPEDIA — Engineer Onboarding Guide

Welcome to MUSICPEDIA! This guide will help you get up to speed quickly so you can start contributing.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [Project Architecture](#project-architecture)
4. [Key Concepts](#key-concepts)
5. [Code Walkthrough](#code-walkthrough)
6. [Running Tests](#running-tests)
7. [Common Tasks](#common-tasks)
8. [Development Workflow](#development-workflow)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, make sure you have:

- **Python 3.x** (tested with 3.9; Python 2.7 also works but is not recommended)
- **pip** (Python package manager)
- **Git**
- A text editor or IDE of your choice (VS Code, PyCharm, etc.)

No external databases or services are needed — the project uses SQLite, which is bundled with Python.

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/verma18/django-project.git
cd django-project
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs Django 1.9.4 (the sole dependency).

### 4. Run database migrations

```bash
python manage.py migrate
```

This creates the SQLite database (`db.sqlite3`) and sets up all tables.

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 6. Start the development server

```bash
python manage.py runserver
```

### 7. Open in your browser

- **App:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Project Architecture

MUSICPEDIA follows Django's **Model-View-Template (MVT)** pattern:

```
django-project/
├── manage.py                  # Django CLI entry point
├── requirements.txt           # Python dependencies (Django==1.9.4)
├── db.sqlite3                 # SQLite database (auto-generated)
│
├── website/                   # Project-level configuration
│   ├── settings.py            # Settings: apps, middleware, DB, static/media paths
│   ├── urls.py                # Root URL router → delegates to music/urls.py
│   └── wsgi.py                # WSGI entry point (for deployment)
│
├── music/                     # The main (and only) Django app
│   ├── models.py              # Data models: Album, Song, Video
│   ├── views.py               # All view functions (request → response)
│   ├── urls.py                # App-level URL patterns
│   ├── forms.py               # ModelForms for Album, Song, Video, User
│   ├── admin.py               # Admin panel registration
│   ├── tests.py               # Unit tests
│   ├── migrations/            # Database schema migrations
│   ├── templates/music/       # HTML templates (Django Template Language)
│   └── static/music/          # CSS, JS, images
│
└── media/                     # User-uploaded files (created at runtime)
```

### How requests flow

```
Browser request
    → website/urls.py (root router)
        → music/urls.py (app router, matches URL pattern)
            → music/views.py (view function processes request)
                → music/models.py (queries/updates database via ORM)
                → music/templates/ (renders HTML response)
    → Browser receives HTML
```

---

## Key Concepts

### Data Models

There are three models, all defined in `music/models.py`:

| Model   | Owned by  | Key relationships                           |
|---------|-----------|----------------------------------------------|
| `Album` | `User`    | Has many `Song`s (ForeignKey from Song)       |
| `Song`  | `Album`   | Belongs to one Album (cascade delete)         |
| `Video` | `User`    | Standalone — not tied to any Album            |

All three models have an `is_favorite` boolean field, toggled via AJAX.

### Authentication

- Django's built-in `django.contrib.auth` handles registration, login, and logout
- Views that require login check `request.user.is_authenticated()` and redirect to the login page if not authenticated
- Each user sees only their own albums, songs, and videos

### File Uploads

- **Albums:** Cover art images (PNG, JPG, JPEG)
- **Songs:** Audio files (WAV, MP3, OGG)
- **Videos:** Video files (MP4, MKV, AVI, MOV, WMV, FLV, WEBM) + optional thumbnail (PNG, JPG, JPEG)
- Uploaded files are stored in the `media/` directory
- File type validation happens in the view functions (not at the model/form level)

### AJAX Favorites

- Clicking the star icon sends a GET request to the favorite endpoint (e.g., `/video/1/favorite/`)
- The view toggles `is_favorite` and returns `{"success": true}` as JSON
- jQuery on the frontend toggles the star icon class without reloading the page
- Implementation is in `music/static/music/js/main.js`

---

## Code Walkthrough

### Adding a new feature (example pattern)

To understand how features are built, trace through the Video feature as a reference:

1. **Model** (`models.py`): `Video` class with fields, `__str__` method
2. **Form** (`forms.py`): `VideoForm` as a `ModelForm` listing editable fields
3. **Views** (`views.py`): Functions for CRUD + favorites + listing
4. **URLs** (`urls.py`): URL patterns mapping regex → view functions
5. **Templates** (`templates/music/`): HTML using Django template tags (`{% for %}`, `{% url %}`, `{% csrf_token %}`)
6. **Admin** (`admin.py`): `admin.site.register(Video)` for admin panel access
7. **JS** (`static/music/js/main.js`): jQuery AJAX for favorites

### Important files to read first

| File                        | Why                                                    |
|-----------------------------|--------------------------------------------------------|
| `music/models.py`           | Understand the data structures                         |
| `music/views.py`            | All business logic lives here                          |
| `music/urls.py`             | See all available endpoints                            |
| `music/templates/music/base.html` | Understand the page layout and navigation       |
| `website/settings.py`       | Understand Django configuration                        |
| `website/urls.py`           | See how the root router delegates to the music app     |

---

## Running Tests

Run the full test suite:

```bash
python manage.py test music
```

For verbose output:

```bash
python manage.py test music --verbosity=2
```

The test suite currently has **30 tests** covering:

| Category     | Count | What's tested                                                    |
|--------------|-------|------------------------------------------------------------------|
| Model tests  | 5     | Creation, `__str__`, defaults, optional fields                   |
| Form tests   | 6     | Valid data, missing required fields, field list                   |
| View tests   | 19    | Login guards, CRUD, file validation, favorites, search, isolation|

### Writing new tests

- Tests live in `music/tests.py`
- Use `django.test.TestCase` as the base class
- Use `django.test.Client` for view tests
- Use `SimpleUploadedFile` for file upload testing
- Follow the existing patterns — see `VideoViewsTest` for comprehensive examples

---

## Common Tasks

### Adding a new model

1. Define the model class in `music/models.py`
2. Create a `ModelForm` in `music/forms.py`
3. Run `python manage.py makemigrations` to generate the migration
4. Run `python manage.py migrate` to apply it
5. Register the model in `music/admin.py`
6. Add views in `music/views.py`
7. Add URL patterns in `music/urls.py`
8. Create templates in `music/templates/music/`
9. Add tests in `music/tests.py`

### Adding a new URL/view

1. Write the view function in `music/views.py`
2. Add a `url()` entry in `music/urls.py` with a regex pattern and name
3. Create or update the template
4. Link to it using `{% url 'music:view_name' %}` in templates

### Modifying the database schema

1. Edit the model in `music/models.py`
2. Run `python manage.py makemigrations`
3. Review the generated migration file in `music/migrations/`
4. Run `python manage.py migrate`

### Adding static files

- Place CSS/JS/images in `music/static/music/`
- Reference them in templates with `{% load staticfiles %}` and `{% static 'music/path/to/file' %}`

---

## Development Workflow

### Branch naming

```
feature/short-description    # New features
fix/short-description        # Bug fixes
```

### Commit checklist

Before committing, make sure:

- [ ] `python manage.py test music` — all tests pass
- [ ] New migrations are committed (if models changed)
- [ ] No `__pycache__/`, `.pyc`, or `db.sqlite3` in your commit
- [ ] No secrets or credentials in the code
- [ ] Templates are consistent with the existing style (Bootstrap 3 + jQuery)

### Code style

- Follow the existing patterns in the codebase
- Views use function-based views (not class-based)
- URLs use `url()` with regex patterns (Django 1.x style)
- Templates extend `base.html` for authenticated pages
- Templates extend `base_visitor.html` for public pages (login, register)

---

## Troubleshooting

### "No module named django"

You haven't activated your virtual environment or haven't installed dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "__classcell__ not set" error

Django 1.9.4 is not compatible with Python 3.10+. Use Python 3.9 or earlier:

```bash
# Using pyenv
pyenv install 3.9.21
pyenv local 3.9.21
```

### Migrations out of sync

If you get database errors after pulling new changes:

```bash
python manage.py migrate
```

If that doesn't work, you can reset (development only):

```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Media files not loading

Make sure `DEBUG = True` in `website/settings.py`. In production, you'd need to configure a web server (Nginx/Apache) to serve media files.

### URL namespace warning

You may see: `URL namespace 'music' isn't unique`. This is a harmless warning caused by the music app being included at both `/music/` and `/` in `website/urls.py`. It doesn't affect functionality.

---

## Need Help?

- Check the [README.md](README.md) for a high-level overview
- Browse `music/views.py` — all business logic is in one file
- Use the Django admin panel (`/admin/`) to inspect and modify data directly
- Run `python manage.py shell` to interactively query the database
