from django.utils.translation import gettext_lazy as _

from debug_toolbar.panels import Panel
from flags.middleware import FlagConditionsMiddleware
from flags.sources import get_flags


class FlagsPanel(Panel):
    """
    A panel to display the current state and conditions of all feature flags
    """

    template = "flags/panels/flags.html"
    title = _("Feature Flags")

    def generate_stats(self, request, response):
        if hasattr(request, FlagConditionsMiddleware.request_attribute):
            flags = getattr(
                request, FlagConditionsMiddleware.request_attribute
            )
        else:
            flags = get_flags()

        self.record_stats(
            {
                'request': request,
                'flags': sorted(flags.values(), key=lambda x: x.name),
            }
        )
