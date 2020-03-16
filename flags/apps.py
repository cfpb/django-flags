from django.apps import AppConfig

from . import checks  # noqa F401


class DjangoFlagsConfig(AppConfig):
    name = "flags"
    verbose_name = "Django Flags"
