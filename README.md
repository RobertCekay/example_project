# Super Blog

A small Django blog app for creating, editing, and deleting posts. Built on Django 6.0 with Bootstrap 5 for styling.

## Requirements

- Python 3.13+
- Django 6.0

## Setup

From the repo root (`django_project/`):

```bash
python -m venv venv
source venv/bin/activate
pip install django
```

## Running the app

```bash
cd example_project
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the post list.

To use the Django admin, create a superuser first:

```bash
python manage.py createsuperuser
```

Then sign in at http://127.0.0.1:8000/admin/.

## Running the tests

From `example_project/`:

```bash
python manage.py test
```

Useful flags:

- `python manage.py test blog` — only the blog app
- `python manage.py test blog.tests.PostCreateViewTests` — a single class
- `-v 2` — verbose output
- `--failfast` — stop on first failure
- `--keepdb` — reuse the test DB between runs

## Project layout

```
example_project/
├── blog/                  # Blog app: models, views, urls, templates, tests
│   ├── templates/blog/    # base.html, home.html, post_form.html, post_delete.html
│   ├── models.py          # Post model
│   ├── views.py           # home + Post Create/Update/Delete class views
│   ├── urls.py            # post/new, post/<pk>/edit, post/<pk>/delete
│   └── tests.py
├── example_project/       # Project settings, root urls, wsgi/asgi
└── manage.py
```

## URLs

| Path | View | Name |
| --- | --- | --- |
| `/` | `home` | `home` |
| `/post/<pk>` | `post_details` | `post-detail` |
| `/post/new/` | `PostCreateView` | `post-create` |
| `/post/<pk>/edit` | `PostUpdateView` | `post-update` |
| `/post/<pk>/delete` | `PostDeleteView` | `post-delete` |
