import re
from distutils.util import strtobool

import django
from django.utils import dateparse, timezone


# This will be maintained by register() as a global dictionary of
# condition_name: [list of functions], so we can have multiple conditions
# for a given name and they all must pass when checking.
CONDITIONS = {}


class DuplicateCondition(ValueError):
    """ Raised when registering a condition that is already registered """


class RequiredForCondition(AttributeError):
    """ Raised when a kwarg that is required for a condition is not given """


def register(condition_name, fn=None):
    """ Register a condition to test for flag state. Can be decorator.
    Conditions can be any callable that takes a value and some number of
    required arguments (specified in 'requires') that were passed as kwargs
    when checking the flag state. """
    global CONDITIONS

    if fn is None:
        # Be a decorator
        def decorator(fn):
            register(condition_name, fn=fn)
            return fn
        return decorator

    # Don't be a decorator, just register
    if condition_name in CONDITIONS:
        raise DuplicateCondition(
            'Flag condition "{name}" already registered.'.format(
                name=condition_name
            )
        )

    CONDITIONS[condition_name] = fn


def get_conditions():
    """ Return the names of all available conditions """
    return CONDITIONS.keys()


def get_condition(condition_name):
    """ Generator to fetch condition checkers from the registry """
    if condition_name in CONDITIONS:
        return CONDITIONS[condition_name]


@register('boolean')
def boolean_condition(condition, **kwargs):
    """ Basic boolean check """
    try:
        return strtobool(condition.strip().lower())
    except AttributeError:
        return bool(condition)


@register('user')
def user_condition(username, request=None, **kwargs):
    """ Does request.user match the expected username? """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'user'")

    return request.user.get_username() == username


@register('anonymous')
def anonymous_condition(boolean_value, request=None, **kwargs):
    """ request.user an anonymous user, true or false based on boolean_value
    """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'anonymous'")

    if django.VERSION[0] >= 2:  # pragma: no cover
        is_anonymous = bool(request.user.is_anonymous)
    else:  # pragma: no cover
        is_anonymous = bool(request.user.is_anonymous())

    try:
        return strtobool(boolean_value.strip().lower()) == is_anonymous
    except AttributeError:
        return bool(boolean_value) == is_anonymous


@register('parameter')
def parameter_condition(param_name, request=None, **kwargs):
    """ Is the parameter name part of the GET parameters? """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'parameter'")
    try:
        param_name, param_value = param_name.split('=')
    except ValueError:
        param_value = 'True'

    return request.GET.get(param_name) == param_value


@register('path matches')
def path_condition(pattern, request=None, **kwargs):
    """ Does the request's path match the given regular expression? """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'path'")

    return bool(re.search(pattern, request.path))


@register('after date')
def after_date_condition(date_or_str, **kwargs):
    """ Is the the current date after the given date?
    date_or_str is either a date object or an ISO 8601 string """
    try:
        date = dateparse.parse_datetime(date_or_str)
    except TypeError:
        date = date_or_str

    now = timezone.now()

    try:
        date_test = (now > date)
    except TypeError:
        date_test = False

    return date_test


# Keeping the old name of this condition function around for
# backwards-compatibility.
date_condition = after_date_condition


@register('before date')
def before_date_condition(date_or_str, **kwargs):
    """ Is the current date before the given date?
    date_or_str is either a date object or an ISO 8601 string """
    try:
        date = dateparse.parse_datetime(date_or_str)
    except TypeError:
        date = date_or_str

    now = timezone.now()

    try:
        date_test = (now < date)
    except TypeError:
        date_test = False

    return date_test
