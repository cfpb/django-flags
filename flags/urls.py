try:
    from django.urls import (
        RegexURLPattern,
        RegexURLResolver
    )
except ImportError:
    from django.core.urlresolvers import (
        RegexURLPattern,
        RegexURLResolver
    )

from flags.decorators import flag_check


class FlaggedURLResolver(RegexURLResolver):
    def __init__(self, flag_name, regex, urlconf_name,
                 default_kwargs=None, app_name=None, namespace=None,
                 state=True, fallback=None):
        super(FlaggedURLResolver, self).__init__(
            regex, urlconf_name, default_kwargs=default_kwargs,
            app_name=app_name, namespace=namespace)
        self.flag_decorator = flag_check(
            flag_name, state, fallback=fallback)

    @property
    def url_patterns(self):
        # Flag each of the resolved URL patterns
        patterns = []
        for pattern in super(FlaggedURLResolver, self).url_patterns:
            flagged_pattern = RegexURLPattern(
                pattern._regex, self.flag_decorator(pattern.callback),
                pattern.default_args, pattern.name)
            patterns.append(flagged_pattern)
        return patterns


def flagged_url(flag_name, regex, view, kwargs=None, name=None,
                state=True, fallback=None):
    """ Make a URL depend on the state of a feature flag """

    if callable(view):
        flagged_view = flag_check(flag_name,
                                  state,
                                  fallback=fallback)(view)
        return RegexURLPattern(regex, flagged_view, kwargs, name)

    elif isinstance(view, (list, tuple)):
        urlconf_module, app_name, namespace = view
        return FlaggedURLResolver(
            flag_name, regex, urlconf_module, kwargs,
            app_name=app_name, namespace=namespace,
            state=state, fallback=fallback)

    else:
        raise TypeError('view must be a callable')
