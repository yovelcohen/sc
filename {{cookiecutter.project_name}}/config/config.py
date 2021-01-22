import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SILK = bool(os.environ.get('SILK', False))

installed_apps = ('django.contrib.admin',
                  'admin_numeric_filter',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django.contrib.postgres',
                  'rest_framework',
                  "rest_framework_api_key",
                  'rest_framework.authtoken',
                  'django_better_admin_arrayfield',
                  'django_singleton_admin',
                  'rangefilter',
                  'corsheaders',
                  'djoser',
                  'api.apps.ConsumerApiConfig',
                  'users',
                  'account_management_api',
                  'drf_spectacular'
                  )

if SILK is True:
    installed_apps += ('silk',)
    middleware = ('corsheaders.middleware.CorsMiddleware',
                  'django.middleware.security.SecurityMiddleware',
                  'django.contrib.sessions.middleware.SessionMiddleware',
                  'django.middleware.common.CommonMiddleware',
                  'django.middleware.csrf.CsrfViewMiddleware',
                  'django.contrib.auth.middleware.AuthenticationMiddleware',
                  'django.contrib.messages.middleware.MessageMiddleware',
                  'silk.middleware.SilkyMiddleware',
                  'django.middleware.clickjacking.XFrameOptionsMiddleware',
                  'whitenoise.middleware.WhiteNoiseMiddleware',
                  )
else:
    middleware = ('corsheaders.middleware.CorsMiddleware',
                  'django.middleware.security.SecurityMiddleware',
                  'django.contrib.sessions.middleware.SessionMiddleware',
                  'django.middleware.common.CommonMiddleware',
                  'django.middleware.csrf.CsrfViewMiddleware',
                  'django.contrib.auth.middleware.AuthenticationMiddleware',
                  'django.contrib.messages.middleware.MessageMiddleware',
                  'django.middleware.clickjacking.XFrameOptionsMiddleware',
                  'whitenoise.middleware.WhiteNoiseMiddleware',
                  )

templates = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR / "templates")],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
)

passwords_validators = (
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
)

rest = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

logging = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'tracibilty-debug.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }

    },

    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

sqlite = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

postgres_details = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mfd_copy',
        'user': 'yovel',
        'PASSWORD': 'HUCKFVIlavoy1',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
use_log_file = '{{cookiecutter.add_file_logger}}'.lower()
handlers = ['console'] if use_log_file == "n" else ['console', 'file']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'tracibilty-debug.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }

    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


class Config:
    WHITH_NOISE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    ALLOWED_HOSTS = ['*']
    STATIC = '/static/'
    UTC = 'UTC'
    EN = 'en-us'
    PASSWORD_VALIDATORS = passwords_validators
    SQLITE_DB = sqlite
    POSTGRES = postgres_details
    AUTH_USER_MODEL = 'users.User'
    WSGI = 'config.wsgi.application'
    TEMPLATES = templates
    URLS = 'config.urls'
    MIDDLEWARE = middleware
    INSTALLED_APPS = installed_apps
    REST_SETTINGS = rest
    SECRET_KEY = 'x2*3)*+!=3ji88w+oz8z%cd0!9(-p1fuje3-dcjl76pwkm)3-)'
    LOGGING = LOGGING
    SILENCED_CHECKS = ['fields.E010', ]


class Docs:
    CAMELIZE_NAMES = 'CAMELIZE_NAMES'
    SECURITY = 'SECURITY'


class Names:
    STATIC = 'static'
    STATIC_FILES = 'staticfiles'
