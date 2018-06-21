from django.apps import AppConfig

from flags.settings import add_flags_from_sources


class DjangoFlagsConfig(AppConfig):
    name = 'flags'
    verbose_name = 'Django Flags'

    def ready(self):
        add_flags_from_sources()
