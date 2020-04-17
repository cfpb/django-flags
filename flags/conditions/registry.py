# These will be maintained by register() as a global dictionary of
# condition_name: function/validator_function
_conditions = {}
_validators = {}


class DuplicateCondition(ValueError):
    """ Raised when registering a condition that is already registered """


def register(condition_name, fn=None, validator=None):
    """ Register a condition to test for flag state. Can be decorator.
    Conditions can be any callable that takes a value and some number of
    required arguments (specified in 'requires') that were passed as kwargs
    when checking the flag state. """
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
            'Flag condition "{name}" already registered.'.format(
                name=condition_name
            )
        )

    _conditions[condition_name] = fn
    _validators[condition_name] = validator


def get_conditions():
    """ Return the names of all available conditions """
    return _conditions.keys()


def get_condition(condition_name):
    """ Fetch condition checker functions from the registry """
    if condition_name in _conditions:
        return _conditions[condition_name]


def get_condition_validator(condition_name):
    """ Fetch condition validators from the registry """
    if condition_name in _validators:
        return _validators[condition_name]
