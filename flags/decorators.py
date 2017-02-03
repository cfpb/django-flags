from django.http import Http404
from django.utils.functional import wraps

from flags.template_functions import flag_enabled


def flag_check(flag_name, condition, alternative=None):
    """ Check that a given flag has the given condition (True/False).
    If the condition is not met, perform the alternative. """
    def decorator(func):
        def inner(request, *args, **kwargs):
            enabled = flag_enabled(request, flag_name)

            if (condition and enabled) or (not condition and not enabled):
                return func(request, *args, **kwargs)
            elif alternative is not None:
                return alternative(request)
            else:
                raise Http404

        return wraps(func)(inner)

    return decorator


def flag_required(flag_name, fallback_view=None, pass_if_set=True):
    return flag_check(flag_name, pass_if_set, alternative=fallback_view)
