from jinja2.ext import Extension

from flags.templatetags.feature_flags import flag_disabled, flag_enabled


try:
    # Jinja 3+
    from jinja2 import pass_context
except ImportError:  # pragma: no cover
    # Jinja 2
    from jinja2 import contextfunction as pass_context


class FlagsExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        self.environment.globals.update(
            {
                "flag_enabled": pass_context(flag_enabled),
                "flag_disabled": pass_context(flag_disabled),
            }
        )


flags = FlagsExtension
