from django.http import Http404
from django.utils.functional import wraps

from flags.state import flag_state


def flag_check(flag_name, state, fallback=None, **fc_kwargs):
    """ Check that a given flag has the given state.
    If the state does not match, perform the fallback. """
    def decorator(func):
        def inner(request, *args, **kwargs):
            enabled = flag_state(flag_name, request=request, **fc_kwargs)

            if ((state and enabled) or (not state and not enabled)):
                return func(request, *args, **kwargs)
            elif fallback is not None:
                return fallback(request, *args, **kwargs)
            else:
                raise Http404

        return wraps(func)(inner)

    return decorator


def flag_required(flag_name, fallback_view=None, pass_if_set=True):
    return flag_check(flag_name, pass_if_set, fallback=fallback_view)
