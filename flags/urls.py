from contextlib import contextmanager

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

        self.flag_name = flag_name
        self.state = state
        self.fallback = fallback
        self.fallback_patterns = []
        if isinstance(self.fallback, (list, tuple)):
            urlconf_module, app_name, namespace = self.fallback
            self.fallback_patterns = RegexURLResolver(
                regex, urlconf_module, None,
                app_name=app_name, namespace=namespace
            ).url_patterns

    @property
    def url_patterns(self):
        # First, add our "positively" flagged URLs, where when the flag
        # matches the defined state, the view is served for the pattern
        # and not the fallback.
        url_patterns = []
        for pattern in super(FlaggedURLResolver, self).url_patterns:
            # Get the fallback view, if there is one, and remove it from
            # the list of fallback patterns.
            fallback = self.fallback
            if isinstance(self.fallback, (list, tuple)):
                fallback = next((p.callback for p in self.fallback_patterns
                                 if p.regex == pattern.regex), None)

            flag_decorator = flag_check(self.flag_name, self.state,
                                        fallback=fallback)
            flagged_pattern = RegexURLPattern(
                pattern.regex.pattern, flag_decorator(pattern.callback),
                pattern.default_args, pattern.name)
            url_patterns.append(flagged_pattern)

        # Next, add "negatively" flagged URLs, where the flag does not match
        # the defined state, for any remaining fallback patterns that didn't
        # match other url patterns.
        url_pattern_regexes = [p.regex for p in url_patterns]
        for pattern in (p for p in self.fallback_patterns
                        if p.regex not in url_pattern_regexes):
            flag_decorator = flag_check(self.flag_name, not self.state)
            flagged_pattern = RegexURLPattern(
                pattern.regex.pattern, flag_decorator(pattern.callback),
                pattern.default_args, pattern.name)
            url_patterns.append(flagged_pattern)

        return url_patterns


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


@contextmanager
def flagged_urls(flag_name, state=True, fallback=None):
    """ Flag multiple URLs in the same context
    Returns a url()-compatible wrapper for flagged_url() """
    def flagged_url_wrapper(regex, view, kwargs=None, name=None):
        return flagged_url(flag_name, regex, view, kwargs=kwargs, name=name,
                           state=state, fallback=fallback)
    yield flagged_url_wrapper
