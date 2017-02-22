from django.conf.urls import url

from flags.decorators import flag_check


def flagged_url(flag_name, regex, view, kwargs=None, name=None,
                condition=True, fallback=None):
    """ Make a URL depend on the state of a feature flag """

    if callable(view):
        flagged_view = flag_check(flag_name,
                                  condition,
                                  fallback=fallback)(view)
        return url(regex, flagged_view, kwargs=kwargs, name=name)

    elif isinstance(view, (list, tuple)):
        # XXX: For right now, we don't support include()
        raise TypeError('Flagged include() is not supported')

    else:
        raise TypeError('view must be a callable')
