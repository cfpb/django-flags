from django.apps import AppConfig

from flags.settings import add_flags_from_sources


class WagtailFlagsConfig(AppConfig):
    name = 'flags'
    verbose_name = 'Wagtail Flags'

    def ready(self):
        add_flags_from_sources()
