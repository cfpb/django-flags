import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import dateparse

from flags.utils import strtobool


validate_parameter = RegexValidator(
    re.compile(r"^[-_\w=]+$"),
    message="Enter a valid HTTP parameter name.",
    code="invalid",
)


def validate_path_re(value):
    try:
        re.compile(value)
    except re.error as e:
        raise ValidationError(
            "Enter either a valid path or a regular expression to match a "
            "path, without a URL scheme, query string, or fragment."
        ) from e


def validate_boolean(value):
    message = "Enter one of 'on', 'off', 'true', 'false', etc."
    try:
        strtobool(value)
    except ValueError as err:
        # This was a string with an invalid boolean value
        raise ValidationError(message) from err
    except AttributeError as err:
        # This was not a string
        if not isinstance(value, (int, bool)):
            raise ValidationError(message) from err


def validate_user(value):
    UserModel = get_user_model()

    try:
        UserModel.objects.get(**{UserModel.USERNAME_FIELD: value})
    except UserModel.DoesNotExist as err:
        raise ValidationError("Enter the username of a valid user.") from err


def validate_date(value):
    datetime = dateparse.parse_datetime(value)
    if datetime is None:
        raise ValidationError("Enter an ISO 8601 date representation.")
