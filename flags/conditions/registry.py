# This will be maintained by register() as the global dictionary of
# condition_name: function
_conditions = {}


class DuplicateCondition(ValueError):
    """Raised when registering a condition that is already registered"""


def register(condition_name, fn=None, validator=None):
    """Register a condition to test for flag state.

    This function can be used as a decorator or the condition callable can be
    passed as `fn`.

    Validators can be passed as a separate callable, `validator`, or can be an
    attribute of the condition callable, fn.validate. If `validator` is
    explicitly given, it will override an existing `validate` attribute of the
    condition callable.

    Conditions can be any callable that takes a value and some number of
    required arguments (specified in 'requires') that were passed as kwargs
    when checking the flag state."""
    global _conditions, _validators

    if fn is None:
        # Be a decorator
        def decorator(fn):
            register(condition_name, fn=fn, validator=validator)
            return fn

        return decorator

    # Don't be a decorator, just register
    if condition_name in _conditions:
        raise DuplicateCondition(
            f'Flag condition "{condition_name}" already registered.'
        )

    # We attach the validator to the callable to allow for both a single source
    # of truth for conditions (_conditions) and to allow for validators to be
    # defined on a callable class along with their condition.
    if validator is not None or not hasattr(fn, "validate"):
        fn.validate = validator

    _conditions[condition_name] = fn


def get_conditions():
    """Return the names of all available conditions"""
    return _conditions.keys()


def get_condition(condition_name):
    """Fetch condition checker functions from the registry"""
    if condition_name in _conditions:
        return _conditions[condition_name]
