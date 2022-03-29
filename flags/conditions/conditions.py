import re

from django.contrib.auth import get_user_model
from django.utils import dateparse, timezone

from flags.conditions.registry import register
from flags.conditions.validators import (
    validate_boolean,
    validate_date,
    validate_parameter,
    validate_path_re,
    validate_user,
)
from flags.utils import strtobool


class RequiredForCondition(AttributeError):
    """Raised when a kwarg that is required for a condition is not given"""


@register("boolean", validator=validate_boolean)
def boolean_condition(condition, **kwargs):
    """Basic boolean check"""
    try:
        return strtobool(condition.strip())
    except AttributeError:
        return bool(condition)


@register("user", validator=validate_user)
def user_condition(username, request=None, **kwargs):
    """Does request.user match the expected username?"""
    if request is None:
        raise RequiredForCondition("request is required for condition 'user'")

    if request.user.is_anonymous:
        return False

    return getattr(request.user, get_user_model().USERNAME_FIELD) == username


@register("anonymous", validator=validate_boolean)
def anonymous_condition(boolean_value, request=None, **kwargs):
    """request.user an anonymous user, true or false based on boolean_value"""
    if request is None:
        raise RequiredForCondition(
            "request is required for condition 'anonymous'"
        )

    is_anonymous = bool(request.user.is_anonymous)

    try:
        return strtobool(boolean_value.strip().lower()) == is_anonymous
    except AttributeError:
        return bool(boolean_value) == is_anonymous


@register("parameter", validator=validate_parameter)
def parameter_condition(param_name, request=None, **kwargs):
    """Is the parameter name part of the GET parameters?"""
    if request is None:
        raise RequiredForCondition(
            "request is required for condition 'parameter'"
        )
    try:
        param_name, param_value = param_name.split("=")
    except ValueError:
        param_value = "True"

    return request.GET.get(param_name) == param_value


@register("path matches", validator=validate_path_re)
def path_condition(pattern, request=None, **kwargs):
    """Does the request's path match the given regular expression?"""
    if request is None:
        raise RequiredForCondition("request is required for condition 'path'")

    return bool(re.search(pattern, request.path))


@register("after date", validator=validate_date)
def after_date_condition(date_or_str, **kwargs):
    """Is the the current date after the given date?
    date_or_str is either a date object or an ISO 8601 string"""
    try:
        date = dateparse.parse_datetime(date_or_str)
    except TypeError:
        date = date_or_str

    now = timezone.now()

    try:
        date_test = now > date
    except TypeError:
        date_test = False

    return date_test


# Keeping the old name of this condition function around for
# backwards-compatibility.
date_condition = after_date_condition


@register("before date", validator=validate_date)
def before_date_condition(date_or_str, **kwargs):
    """Is the current date before the given date?
    date_or_str is either a date object or an ISO 8601 string"""
    try:
        date = dateparse.parse_datetime(date_or_str)
    except TypeError:
        date = date_or_str

    now = timezone.now()

    try:
        date_test = now < date
    except TypeError:
        date_test = False

    return date_test
