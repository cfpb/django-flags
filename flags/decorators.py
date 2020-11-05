import inspect
import warnings

from django.http import Http404
from django.utils.functional import wraps

from flags.state import flag_state


def flag_check(flag_name, state, fallback=None, **fc_kwargs):
    """Check that a given flag has the given state.
    If the state does not match, perform the fallback."""

    def decorator(func):
        """
        Decorator for decorate a function.

        Args:
            func: (todo): write your description
        """
        # At decoration-time, ensure that the fallback for the decorated
        # function has the same argspec
        if fallback is not None:
            func_argspec = inspect.getfullargspec(func)
            fallback_argspec = inspect.getfullargspec(fallback)

            if func_argspec.args != fallback_argspec.args:
                warnings.warn(
                    "Feature flag check fallback for "
                    + func.__name__
                    + " takes different arguments.",
                    RuntimeWarning,
                    stacklevel=2,
                )

        def inner(request, *args, **kwargs):
            """
            Decorator for django. http.

            Args:
                request: (todo): write your description
            """
            enabled = flag_state(flag_name, request=request, **fc_kwargs)

            if (state and enabled) or (not state and not enabled):
                return func(request, *args, **kwargs)
            elif fallback is not None:
                return fallback(request, *args, **kwargs)
            else:
                raise Http404

        return wraps(func)(inner)

    return decorator


def flag_required(flag_name, fallback_view=None, pass_if_set=True):
    """
    Decorator to set a flag on the default flag.

    Args:
        flag_name: (str): write your description
        fallback_view: (todo): write your description
        pass_if_set: (str): write your description
    """
    return flag_check(flag_name, pass_if_set, fallback=fallback_view)
