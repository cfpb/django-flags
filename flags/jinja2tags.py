from jinja2.ext import Extension

from flags.templatetags.feature_flags import flag_disabled, flag_enabled

try:
    # Jinja2 3.0+
    from jinja2 import pass_context
except ImportError:
    from jinja2 import contextfunction as pass_context


class FlagsExtension(Extension):
    def __init__(self, environment):
        super(FlagsExtension, self).__init__(environment)
        self.environment.globals.update(
            {
                "flag_enabled": pass_context(flag_enabled),
                "flag_disabled": pass_context(flag_disabled),
            }
        )


flags = FlagsExtension
