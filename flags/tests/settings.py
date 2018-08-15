from __future__ import absolute_import, unicode_literals

import os

import django


SECRET_KEY = 'not needed'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'DATABASE_ENGINE',
            'django.db.backends.sqlite3'
        ),
        'NAME': os.environ.get('DATABASE_NAME', 'flagstest.sqlite'),
        'USER': os.environ.get('DATABASE_USER', None),
        'PASSWORD': os.environ.get('DATABASE_PASS', None),
        'HOST': os.environ.get('DATABASE_HOST', None),

        'TEST': {
            'NAME': os.environ.get('DATABASE_NAME', None),
        },
    },
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
)

INSTALLED_APPS += (
    'flags',
)

if django.VERSION >= (1, 10):  # pragma: no cover
    MIDDLEWARE = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    )
else:  # pragma: no cover
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    )

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
        ],
    }
}]

FLAGS = {
    'FLAG_ENABLED': {'boolean': True},
    'FLAG_ENABLED2': {'boolean': True},
    'FLAG_DISABLED': {'boolean': False},
    'DB_FLAG': {},
}
