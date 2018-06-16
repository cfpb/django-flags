from contextlib import contextmanager
from functools import partial

import django

from flags.decorators import flag_check


try:  # pragma: no cover
    from django.urls.resolvers import (
        RegexPattern,
        RoutePattern,
        URLPattern,
        URLResolver
    )
except ImportError:  # pragma: no cover
    from django.core.urlresolvers import (
        RegexURLPattern as URLPattern,
        RegexURLResolver as URLResolver
    )


class FlaggedURLResolver(URLResolver):
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
            self.fallback_patterns = URLResolver(
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
                if django.VERSION[0] >= 2:
                    fallback = next((
                        p.callback for p in self.fallback_patterns
                        if p.pattern.describe() == pattern.pattern.describe()
                    ), None)
                else:
                    fallback = next((
                        p.callback for p in self.fallback_patterns
                        if p.regex == pattern.regex
                    ), None)

            flag_decorator = flag_check(self.flag_name, self.state,
                                        fallback=fallback)

            if django.VERSION[0] >= 2:
                route_pattern = pattern.pattern
            else:
                route_pattern = pattern.regex.pattern

            flagged_pattern = URLPattern(
                route_pattern, flag_decorator(pattern.callback),
                pattern.default_args, pattern.name)

            url_patterns.append(flagged_pattern)

        # Next, add "negatively" flagged URLs, where the flag does not match
        # the defined state, for any remaining fallback patterns that didn't
        # match other url patterns.
        if django.VERSION[0] >= 2:
            # Django >= 2.0
            described_patterns = [p.pattern.describe() for p in url_patterns]
            negative_patterns = (
                p for p in self.fallback_patterns
                if p.pattern.describe() not in described_patterns
            )
        else:
            described_patterns = [p.regex for p in url_patterns]
            negative_patterns = (
                p for p in self.fallback_patterns
                if p.regex not in described_patterns
            )

        for pattern in negative_patterns:
            flag_decorator = flag_check(self.flag_name, not self.state)

            if django.VERSION[0] >= 2:
                route_pattern = pattern.pattern
            else:
                route_pattern = pattern.regex.pattern

            flagged_pattern = URLPattern(
                route_pattern, flag_decorator(pattern.callback),
                pattern.default_args, pattern.name)

            url_patterns.append(flagged_pattern)

        return url_patterns


def _flagged_path(flag_name, route, view, kwargs=None, name=None,
                  state=True, fallback=None, Pattern=None):
    """ Make a URL depend on the state of a feature flag """
    if callable(view):
        flagged_view = flag_check(flag_name,
                                  state,
                                  fallback=fallback)(view)

        if Pattern:
            route_pattern = Pattern(route, name=name, is_endpoint=True)
        else:
            route_pattern = route

        return URLPattern(route_pattern, flagged_view, kwargs, name)

    elif isinstance(view, (list, tuple)):
        urlconf_module, app_name, namespace = view

        if Pattern:
            route_pattern = Pattern(route, name=name, is_endpoint=True)
        else:
            route_pattern = route

        return FlaggedURLResolver(
            flag_name, route_pattern, urlconf_module, kwargs,
            app_name=app_name, namespace=namespace,
            state=state, fallback=fallback)

    else:
        raise TypeError('view must be a callable')


@contextmanager
def _flagged_paths(flag_name, state=True, fallback=None, Pattern=None):
    """ Flag multiple URLs in the same context
    Returns a url()-compatible wrapper for flagged_url() """
    def flagged_url_wrapper(route, view, kwargs=None, name=None):
        return _flagged_path(flag_name, route, view, kwargs=kwargs, name=name,
                             state=state, fallback=fallback, Pattern=Pattern)
    yield flagged_url_wrapper


if django.VERSION[0] >= 2:
    flagged_path = partial(_flagged_path, Pattern=RoutePattern)
    flagged_re_path = partial(_flagged_path, Pattern=RegexPattern)
    flagged_paths = partial(_flagged_paths, Pattern=RoutePattern)
    flagged_re_paths = partial(_flagged_paths, Pattern=RegexPattern)
else:
    flagged_url = partial(_flagged_path, Pattern=None)
    flagged_urls = partial(_flagged_paths, Pattern=None)
