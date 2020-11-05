import logging

from django.utils.translation import gettext_lazy as _

from debug_toolbar.panels import Panel

from flags import state
from flags.sources import get_flags


logger = logging.getLogger(__name__)

_original_flag_state = state._flag_state


class FlagsPanel(Panel):
    """
    A panel to display the current state and conditions of all feature flags
    """

    template = "flags/panels/flags.html"
    title = _("Feature Flags")

    def generate_stats(self, request, response):
        """
        Generate stats.

        Args:
            self: (todo): write your description
            request: (todo): write your description
            response: (todo): write your description
        """
        flags = get_flags(request=request)

        self.record_stats(
            {
                "request": request,
                "flags": sorted(flags.values(), key=lambda x: x.name),
            }
        )


class FlagChecksPanel(Panel):
    """
    A panel to display the current state and conditions of all feature flags
    """

    template = "flags/panels/flag_checks.html"
    title = _("Flag Checks")

    def __init__(self, *args, **kwargs):
        """
        Initialize the checks.

        Args:
            self: (todo): write your description
        """
        super(FlagChecksPanel, self).__init__(*args, **kwargs)
        self.checks = {}

    def enable_instrumentation(self):
        """
        Enables the instrument instrument flag.

        Args:
            self: (todo): write your description
        """
        # Monkey-patch flag checking to record where the call happens
        def recording_flag_state(flag_name, **kwargs):
            """
            Returns a list of checksum of the given flag.

            Args:
                flag_name: (str): write your description
            """
            if flag_name not in self.checks:
                self.checks[flag_name] = []

            result = _original_flag_state(flag_name, **kwargs)

            self.checks[flag_name].append(result)

            return result

        state._flag_state = recording_flag_state

    def disable_instrumentation(self):
        """
        Disable the instrumentation.

        Args:
            self: (todo): write your description
        """
        # Restore the original functions
        state._flag_state = _original_flag_state

    def generate_stats(self, request, response):
        """
        Generate the statistics object.

        Args:
            self: (todo): write your description
            request: (todo): write your description
            response: (todo): write your description
        """
        self.record_stats({"request": request, "checks": self.checks})
