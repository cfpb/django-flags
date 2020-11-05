from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from flags.conditions.validators import (
    validate_boolean,
    validate_date,
    validate_parameter,
    validate_path,
    validate_user,
)


class ValidateParameterTestCase(TestCase):
    def test_invalid_parameter_strings(self):
        """
        Validate that all of the strings in a list of strings.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValidationError):
            validate_parameter("%20flag")

    def test_valid_parameter_strings(self):
        """
        Validate that all of the parameters.

        Args:
            self: (todo): write your description
        """
        validate_parameter("myflag")
        validate_parameter("my-flag")
        validate_parameter("my_flag")
        validate_parameter("my_flag=enable")
        validate_parameter("myflág")
        validate_parameter("myflág0")


class ValidatePathTestCase(TestCase):
    def test_invalid_path_strings(self):
        """
        Validate that all paths invalidations are valid.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValidationError):
            validate_path("/my/path#foo")
        with self.assertRaises(ValidationError):
            validate_path("/my/path?foo=bar")
        with self.assertRaises(ValidationError):
            validate_path("https://foo/my/path")

    def test_valid_path_strings(self):
        """
        Validate that the given string is valid.

        Args:
            self: (todo): write your description
        """
        validate_path("/my/path")
        validate_path("/my/path/")
        validate_path("my/path/")


class ValidateBooleanTestCase(TestCase):
    def test_invalid_boolean_strings(self):
        """ ValidationError should be raised for invalid boolean values """
        with self.assertRaises(ValidationError):
            validate_boolean("Flase")
        with self.assertRaises(ValidationError):
            validate_boolean("Ture")
        with self.assertRaises(ValidationError):
            validate_boolean("  True")
        with self.assertRaises(ValidationError):
            validate_boolean("True ")
        with self.assertRaises(ValidationError):
            validate_boolean(["foo"])

    def test_valid_boolean_strings(self):
        """ Valid boolean values should not raise ValidationError """
        validate_boolean(True)
        validate_boolean(False)
        validate_boolean(1)
        validate_boolean(0)
        validate_boolean("true")


class ValidateUserTestCase(TestCase):
    def test_invalid_user(self):
        """
        Validate the user is valid.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValidationError):
            validate_user("nottestuser")

    def test_valid_user(self):
        """
        Validate the user

        Args:
            self: (todo): write your description
        """
        User = get_user_model()
        User.objects.create_user(username="testuser", email="test@user")
        validate_user("testuser")

    @override_settings(AUTH_USER_MODEL="testapp.MyUserModel")
    def test_custom_user_valid(self):
        """
        Test if user is_valid_user.

        Args:
            self: (todo): write your description
        """
        User = get_user_model()
        u = User(identifier="customuser")
        u.save()
        validate_user("customuser")

    @override_settings(AUTH_USER_MODEL="testapp.MyUserModel")
    def test_custom_user_invalid(self):
        """
        Validate user is valid.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValidationError):
            validate_user("nottestuser")


class ValidateDateTestCase(TestCase):
    def test_invalid_date_strings(self):
        """
        Validate that the date is in the correct date.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValidationError):
            validate_date("tomorrowish")
        with self.assertRaises(ValidationError):
            validate_date("2020-04-01")

    def test_valid_date_strings(self):
        """
        Validate that the date string.

        Args:
            self: (todo): write your description
        """
        validate_date("2020-04-01T12:00")
        validate_date("2020-04-01T12:00+04:00")
