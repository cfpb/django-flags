import os

from django.urls import include, path

import debug_toolbar

from flags.conditions import register


SECRET_KEY = "not needed"

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "DATABASE_ENGINE", "django.db.backends.sqlite3"
        ),
        "NAME": os.environ.get("DATABASE_NAME", "flagstest.sqlite"),
        "USER": os.environ.get("DATABASE_USER", None),
        "PASSWORD": os.environ.get("DATABASE_PASS", None),
        "HOST": os.environ.get("DATABASE_HOST", None),
        "TEST": {"NAME": os.environ.get("DATABASE_NAME", None)},
    },
}

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "debug_toolbar",
)

INSTALLED_APPS += ("flags", "flags.tests.testapp")

MIDDLEWARE = (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

STATIC_URL = "/static/"

USE_TZ = True

FLAGS = {
    "FLAG_ENABLED": [("boolean", True)],
    "FLAG_ENABLED_WITH_KWARG": [("flag_enabled_with_kwarg", (2 + 2))],
    "FLAG_DISABLED": [("boolean", False)],
    "DB_FLAG": [],
}

DEBUG_TOOLBAR_PANELS = [
    "flags.panels.FlagsPanel",
    "flags.panels.FlagChecksPanel",
]


@register("flag_enabled_with_kwarg")
def kwarg_condition(expected_value, passed_value=None, **kwargs):
    """Checks that an expected value matches a passed value"""
    return expected_value == passed_value


# DEBUG=True
# INTERNAL_IPS=['127.0.0.1']
ROOT_URLCONF = __name__


urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
]
