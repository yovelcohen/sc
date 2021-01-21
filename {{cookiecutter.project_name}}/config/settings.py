import os
from pathlib import Path
from typing import Dict, Any

import django_heroku

from config.config import Config, Docs, Names, SILK

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = Config.SECRET_KEY

DEBUG = True

INSTALLED_APPS = Config.INSTALLED_APPS

MIDDLEWARE = Config.MIDDLEWARE

SPECTACULAR_DEFAULTS: Dict[str, Any] = {
    Docs.CAMELIZE_NAMES: False,
    Docs.SECURITY: None,
    'TITLE': '{{cookiecutter.project_slug_name}}',
    'DESCRIPTION': '{{cookiecutter.project_slug_name}} Docs',
    'VERSION': '1.0.0'
}

ALLOWED_HOSTS = Config.ALLOWED_HOSTS
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = Config.ALLOWED_HOSTS

ROOT_URLCONF = Config.URLS

TEMPLATES = Config.TEMPLATES

WSGI_APPLICATION = Config.WSGI

REST_FRAMEWORK = Config.REST_SETTINGS

DATABASES = Config.SQLITE_DB

AUTH_USER_MODEL = Config.AUTH_USER_MODEL

AUTH_PASSWORD_VALIDATORS = Config.PASSWORD_VALIDATORS

LANGUAGE_CODE = Config.EN

TIME_ZONE = Config.UTC

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_STORAGE = Config.WHITH_NOISE

STATIC_ROOT = os.path.join(BASE_DIR, Names.STATIC_FILES)

STATIC_URL = Config.STATIC

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, Names.STATIC),
)

LOGGING = Config.LOGGING

SILENCED_SYSTEM_CHECKS = Config.SILENCED_CHECKS

if SILK is True:
    SILKY_PYTHON_PROFILER = True
    SILKY_ANALYZE_QUERIES = True

django_heroku.settings(locals(), logging=False)
