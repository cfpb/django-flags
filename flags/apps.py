from django.apps import AppConfig

from . import checks  # noqa F401


class DjangoFlagsConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "flags"
    verbose_name = "Django Flags"
