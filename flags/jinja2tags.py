from jinja2 import contextfunction
from jinja2.ext import Extension

from flags.templatetags.feature_flags import flag_disabled, flag_enabled


class FlagsExtension(Extension):
    def __init__(self, environment):
        """
        Initialize the environment.

        Args:
            self: (todo): write your description
            environment: (todo): write your description
        """
        super(FlagsExtension, self).__init__(environment)
        self.environment.globals.update(
            {
                "flag_enabled": contextfunction(flag_enabled),
                "flag_disabled": contextfunction(flag_disabled),
            }
        )


flags = FlagsExtension
