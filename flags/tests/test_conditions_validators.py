import django
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from flags.conditions.validators import (
    validate_boolean,
    validate_date,
    validate_parameter,
    validate_path_re,
    validate_user,
)


class ValidateParameterTestCase(TestCase):
    def test_invalid_parameter_strings(self):
        with self.assertRaises(ValidationError):
            validate_parameter("%20flag")

    def test_valid_parameter_strings(self):
        validate_parameter("myflag")
        validate_parameter("my-flag")
        validate_parameter("my_flag")
        validate_parameter("my_flag=enable")
        validate_parameter("myflág")
        validate_parameter("myflág0")


class ValidatePathTestCase(TestCase):
    def test_invalid_path_regexs(self):
        with self.assertRaises(ValidationError):
            validate_path_re("*foo/my/path")

    def test_valid_path_regexs(self):
        validate_path_re("/my/path")
        validate_path_re("/my/path/")
        validate_path_re("my/path/")
        validate_path_re(r"^/my/(path)?$")


class ValidateBooleanTestCase(TestCase):
    def test_invalid_boolean_strings(self):
        """ValidationError should be raised for invalid boolean values"""
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
        """Valid boolean values should not raise ValidationError"""
        validate_boolean(True)
        validate_boolean(False)
        validate_boolean(1)
        validate_boolean(0)
        validate_boolean("true")


class ValidateUserTestCase(TestCase):
    def test_invalid_user(self):
        with self.assertRaises(ValidationError):
            validate_user("nottestuser")

    def test_valid_user(self):
        User = get_user_model()
        User.objects.create_user(username="testuser", email="test@user")
        validate_user("testuser")

    @override_settings(AUTH_USER_MODEL="testapp.MyUserModel")
    def test_custom_user_valid(self):
        User = get_user_model()
        u = User(identifier="customuser")
        u.save()
        validate_user("customuser")

    @override_settings(AUTH_USER_MODEL="testapp.MyUserModel")
    def test_custom_user_invalid(self):
        with self.assertRaises(ValidationError):
            validate_user("nottestuser")


class ValidateDateTestCase(TestCase):
    def test_invalid_date_strings(self):
        with self.assertRaises(ValidationError):
            validate_date("tomorrowish")

        # Django 4.0 relies on Python 3.7+'s `datetime.fromisoformat()`, which
        # handles this where the old regex did not. This is now valid when on
        # Django 4.0+. See https://github.com/django/django/pull/14582
        if django.VERSION < (4, 0):
            with self.assertRaises(ValidationError):
                validate_date("2020-04-01")

    def test_valid_date_strings(self):
        validate_date("2020-04-01T12:00")
        validate_date("2020-04-01T12:00+04:00")
