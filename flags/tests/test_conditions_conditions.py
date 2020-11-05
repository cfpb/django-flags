from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest, QueryDict
from django.test import TestCase, override_settings
from django.utils import timezone

from flags.conditions.conditions import (
    RequiredForCondition,
    after_date_condition,
    anonymous_condition,
    before_date_condition,
    boolean_condition,
    parameter_condition,
    path_condition,
    user_condition,
)


class BooleanConditionTestCase(TestCase):
    def test_boolean_condition_valid(self):
        """
        Validate that the condition is true.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(boolean_condition(True))

    def test_boolean_condition_invalid(self):
        """
        Validate that the condition is true.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(boolean_condition(False))

    def test_boolean_condition_valid_string(self):
        """
        Set the condition condition condition condition

        Args:
            self: (todo): write your description
        """
        self.assertTrue(boolean_condition("True"))
        self.assertTrue(boolean_condition("true"))
        self.assertTrue(boolean_condition("t"))
        self.assertTrue(boolean_condition("yes"))
        self.assertTrue(boolean_condition("y"))
        self.assertTrue(boolean_condition("on"))
        self.assertTrue(boolean_condition("1"))
        self.assertTrue(boolean_condition("true"))
        self.assertTrue(boolean_condition("true   "))

    def test_boolean_condition_invalid_string(self):
        """
        Set condition condition condition condition.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(boolean_condition("False"))
        self.assertFalse(boolean_condition("false"))
        self.assertFalse(boolean_condition("f"))
        self.assertFalse(boolean_condition("no"))
        self.assertFalse(boolean_condition("n"))
        self.assertFalse(boolean_condition("off"))
        self.assertFalse(boolean_condition("0"))


class UserConditionTestCase(TestCase):
    def setUp(self):
        """
        Set the current user for this user

        Args:
            self: (todo): write your description
        """
        user = User.objects.create_user(username="testuser", email="test@user")
        self.request = HttpRequest()
        self.request.user = user

    def test_user_valid(self):
        """
        Validate the condition is valid.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(user_condition("testuser", request=self.request))

    def test_user_invalid(self):
        """
        Validate that the user is in test.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(user_condition("nottestuser", request=self.request))

    def test_request_required(self):
        """
        Test if the request condition.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(RequiredForCondition):
            user_condition("testuser")

    @override_settings(AUTH_USER_MODEL="testapp.MyUserModel")
    def test_custom_user_model_valid(self):
        """
        Validate the user fields.

        Args:
            self: (todo): write your description
        """
        user = get_user_model()(identifier="customuser")
        user.save()
        self.request.user = user
        self.assertTrue(user_condition("customuser", request=self.request))


class AnonymousConditionTestCase(TestCase):
    def setUp(self):
        """
        Sets the request.

        Args:
            self: (todo): write your description
        """
        self.request = HttpRequest()

    def test_anonymous_valid(self):
        """
        Test if the user is authorized.

        Args:
            self: (todo): write your description
        """
        self.request.user = AnonymousUser()
        self.assertTrue(anonymous_condition(True, request=self.request))

    def test_anonymous_invalid(self):
        """
        Test if the user is in the request.

        Args:
            self: (todo): write your description
        """
        user = User.objects.create_user(
            username="notadminuser", email="test@user"
        )
        self.request.user = user
        self.assertFalse(anonymous_condition(True, request=self.request))

    def test_request_required(self):
        """
        Assert that the condition condition.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(RequiredForCondition):
            anonymous_condition(True)


class ParameterConditionTestCase(TestCase):
    def setUp(self):
        """
        Sets the request.

        Args:
            self: (todo): write your description
        """
        self.request = HttpRequest()

    def test_parameter_condition_valid(self):
        """
        Validate condition condition condition condition.

        Args:
            self: (todo): write your description
        """
        self.request.GET = QueryDict("my_flag=True")
        self.assertTrue(parameter_condition("my_flag", request=self.request))

        self.request.GET = QueryDict("my_flag=today")
        self.assertTrue(
            parameter_condition("my_flag=today", request=self.request)
        )

        self.request.GET = QueryDict("my_flag")
        self.assertTrue(parameter_condition("my_flag=", request=self.request))

    def test_parameter_condition_non_existent(self):
        """
        Test the condition condition condition.

        Args:
            self: (todo): write your description
        """
        self.request.GET = QueryDict("my_flag=True")
        self.assertFalse(
            parameter_condition("my_flag=false", request=self.request)
        )

        self.request.GET = QueryDict("my_flag=True")
        self.assertFalse(
            parameter_condition("my_flag=today", request=self.request)
        )

        self.request.GET = QueryDict("my_flag")
        self.assertFalse(parameter_condition("my_flag", request=self.request))

        self.request.GET = QueryDict("")
        self.assertFalse(parameter_condition("my_flag=", request=self.request))

    def test_request_required(self):
        """
        Assert that the condition is required.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(RequiredForCondition):
            parameter_condition("my_flag")


class PathConditionTestCase(TestCase):
    def setUp(self):
        """
        Sets the request.

        Args:
            self: (todo): write your description
        """
        self.request = HttpRequest()

    def test_path_condition_valid_exact(self):
        """
        Validate the condition condition condition.

        Args:
            self: (todo): write your description
        """
        self.request.path = "/my/path"
        self.assertTrue(path_condition("/my/path", request=self.request))

    def test_path_condition_valid_subpath(self):
        """
        Validate condition condition condition condition.

        Args:
            self: (todo): write your description
        """
        self.request.path = "/my/path/to/somewhere"
        self.assertTrue(path_condition("/my/path", request=self.request))

    def test_path_condition_valid_not_starting_with(self):
        """
        Validate that the condition condition condition exists.

        Args:
            self: (todo): write your description
        """
        self.request.path = "/subsection/my/path"
        self.assertTrue(path_condition("/my/path", request=self.request))

    def test_path_condition_invalid(self):
        """
        Ensure that the condition exists.

        Args:
            self: (todo): write your description
        """
        self.request.path = "/your/path"
        self.assertFalse(path_condition("/my/path", request=self.request))

    def test_request_required(self):
        """
        Assert that the condition is required.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(RequiredForCondition):
            path_condition("/my/path")


class AfterDateConditionTestCase(TestCase):
    def setUp(self):
        """
        Sets the timedelta.

        Args:
            self: (todo): write your description
        """
        # Set up some datetimes relative to now for testing
        delta = timedelta(days=1)

        self.past_datetime_tz = timezone.now() - delta
        self.past_datetime_notz = self.past_datetime_tz.replace(tzinfo=None)
        self.past_datetime_tz_str = self.past_datetime_tz.isoformat()
        self.past_datetime_notz_str = self.past_datetime_notz.isoformat()

        self.future_datetime_tz = timezone.now() + delta
        self.future_datetime_notz = self.future_datetime_tz.replace(
            tzinfo=None
        )
        self.future_datetime_tz_str = self.future_datetime_tz.isoformat()
        self.future_datetime_notz_str = self.future_datetime_notz.isoformat()

    def test_date_timeone_true(self):
        """
        Test if the condition to true is true is true is true false otherwise.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(after_date_condition(self.past_datetime_tz))

    def test_date_no_timeone_true(self):
        """
        Test if the condition is true.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(after_date_condition(self.past_datetime_notz))

    def test_date_str_timeone_true(self):
        """
        Test if the given date is true.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(after_date_condition(self.past_datetime_tz_str))

    def test_date_str_no_timeone_true(self):
        """
        Test if the date is true.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(after_date_condition(self.past_datetime_notz_str))

    def test_date_timeone_false(self):
        """
        Test if the future is still alive.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(after_date_condition(self.future_datetime_tz))

    def test_date_no_timeone_false(self):
        """
        Test if the future is still alive.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(after_date_condition(self.future_datetime_notz))

    def test_date_str_timeone_false(self):
        """
        Test if the future was received.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(after_date_condition(self.future_datetime_tz_str))

    def test_date_str_no_timeone_false(self):
        """
        Sets the condition is alive.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(after_date_condition(self.future_datetime_notz_str))

    def test_not_valid_date_str(self):
        """
        Validate that the date is valid.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(after_date_condition("I am not a valid date"))


class BeforeDateConditionTestCase(TestCase):
    def setUp(self):
        """
        Sets the timedelta.

        Args:
            self: (todo): write your description
        """
        # Set up some datetimes relative to now for testing
        delta = timedelta(days=1)

        self.past_datetime_tz = timezone.now() - delta
        self.past_datetime_notz = self.past_datetime_tz.replace(tzinfo=None)
        self.past_datetime_tz_str = self.past_datetime_tz.isoformat()
        self.past_datetime_notz_str = self.past_datetime_notz.isoformat()

        self.future_datetime_tz = timezone.now() + delta
        self.future_datetime_notz = self.future_datetime_tz.replace(
            tzinfo=None
        )
        self.future_datetime_tz_str = self.future_datetime_tz.isoformat()
        self.future_datetime_notz_str = self.future_datetime_notz.isoformat()

    def test_date_timeone_true(self):
        """
        Test if the condition is true.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(before_date_condition(self.future_datetime_tz))

    def test_date_no_timeone_true(self):
        """
        Test if the given date is true.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(before_date_condition(self.future_datetime_notz))

    def test_date_str_timeone_true(self):
        """
        Sets the condition is true.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(before_date_condition(self.future_datetime_tz_str))

    def test_date_str_no_timeone_true(self):
        """
        Sets the date is true.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(before_date_condition(self.future_datetime_notz_str))

    def test_date_timeone_false(self):
        """
        Test if the given date is false.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(before_date_condition(self.past_datetime_tz))

    def test_date_no_timeone_false(self):
        """
        Test if the given date is not empty.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(before_date_condition(self.past_datetime_notz))

    def test_date_str_timeone_false(self):
        """
        Test if the date is a string.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(before_date_condition(self.past_datetime_tz_str))

    def test_date_str_no_timeone_false(self):
        """
        Test if the date is in the string.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(before_date_condition(self.past_datetime_notz_str))

    def test_not_valid_date_str(self):
        """
        Validate the date is valid.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(before_date_condition("I am not a valid date"))
