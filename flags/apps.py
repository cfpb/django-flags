from django.apps import AppConfig
from django.conf import settings
from django.core.cache import cache

from flags.settings import add_flags_from_sources


class DjangoFlagsConfig(AppConfig):
    name = 'flags'
    verbose_name = 'Django Flags'

    def ready(self):
        # Clear any cached flag conditions
        FLAGS_CACHE_KEY = getattr(settings, 'FLAGS_CACHE_KEY', 'flags')
        cache.delete(FLAGS_CACHE_KEY)

        add_flags_from_sources()
