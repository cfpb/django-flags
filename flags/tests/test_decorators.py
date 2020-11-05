import warnings
from unittest.mock import Mock

from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase

from flags.decorators import flag_check, flag_required


class FlagCheckTestCase(TestCase):
    def setUp(self):
        """
        Sets the mocker.

        Args:
            self: (todo): write your description
        """
        self.request = HttpRequest()
        self.request.META["SERVER_NAME"] = "localhost"
        self.request.META["SERVER_PORT"] = 8000

        self.mock_view = Mock(__name__="view")
        self.view = lambda request: self.mock_view(request)

    def test_decorated_no_flag_exists(self):
        """
        Decorator to test whether or not.

        Args:
            self: (todo): write your description
        """
        decorated = flag_check("FLAG_DOES_NOT_EXIST", True)(self.view)
        with self.assertRaises(Http404):
            decorated(self.request)
        self.assertEqual(self.mock_view.call_count, 0)

    def test_decorated_flag_disabled(self):
        """
        Called when the test was called.

        Args:
            self: (todo): write your description
        """
        decorated = flag_check("FLAG_DISABLED", True)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.mock_view.call_count, 0)

    def test_decorated_flag_enabled(self):
        """
        Decorator that registers a flask response.

        Args:
            self: (todo): write your description
        """
        def view(request):
            """
            Displays the view.

            Args:
                request: (todo): write your description
            """
            return HttpResponse("ok")

        decorated = flag_check("FLAG_ENABLED", True)(view)
        response = decorated(self.request)
        self.assertContains(response, "ok")

    def test_fallback_view(self):
        """
        Decorator that the fallback to fallback.

        Args:
            self: (todo): write your description
        """
        def fallback(request, **kwargs):
            """
            Decorator for django.

            Args:
                request: (todo): write your description
            """
            return HttpResponse("fallback")

        decorator = flag_check("FLAG_DISABLED", True, fallback=fallback)
        decorated = decorator(self.view)
        response = decorated(self.request)
        self.assertContains(response, "fallback")

    def test_pass_if_not_set_no_flag_exists(self):
        """
        This decorator is_pass_notfound.

        Args:
            self: (todo): write your description
        """
        def view(request):
            """
            Displays the view.

            Args:
                request: (todo): write your description
            """
            return HttpResponse("ok")

        decorated = flag_check("FLAG_DOES_NOT_EXIST", False)(view)
        response = decorated(self.request)
        self.assertContains(response, "ok")

    def test_pass_if_not_set_disabled(self):
        """
        Decorator to set a response is not allowed to true.

        Args:
            self: (todo): write your description
        """
        def view(request):
            """
            Displays the view.

            Args:
                request: (todo): write your description
            """
            return HttpResponse("ok")

        decorated = flag_check("FLAG_DISABLED", False)(view)
        response = decorated(self.request)
        self.assertContains(response, "ok")

    def test_pass_if_not_set_enabled(self):
        """
        Test if the request is enabled.

        Args:
            self: (todo): write your description
        """
        decorated = flag_check("FLAG_ENABLED", False)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.mock_view.call_count, 0)

    def test_pass_if_not_set_fallback_view(self):
        """
        Decorator to set the default passback to the default test.

        Args:
            self: (todo): write your description
        """
        def fallback(request, **kwargs):
            """
            Decorator for django.

            Args:
                request: (todo): write your description
            """
            return HttpResponse("fallback")

        decorator = flag_check(
            "FLAG_ENABLED",
            False,
            fallback=fallback,
        )

        decorated = decorator(self.view)
        response = decorated(self.request)
        self.assertContains(response, "fallback")

    def test_flag_required(self):
        """
        Decorator to protect a request.

        Args:
            self: (todo): write your description
        """
        def view(request):
            """
            Displays the view.

            Args:
                request: (todo): write your description
            """
            return HttpResponse("ok")

        decorated = flag_required("FLAG_ENABLED")(view)
        response = decorated(self.request)
        self.assertContains(response, "ok")

    def test_view_fallback_different_args(self):
        """
        Decorator to - fallback - in the future.

        Args:
            self: (todo): write your description
        """
        def view(request, extra_arg, kwarg=None):
            """
            View the given the request.

            Args:
                request: (todo): write your description
                extra_arg: (str): write your description
                kwarg: (todo): write your description
            """
            return HttpResponse("ok")  # pragma: no cover

        def fallback(request):
            """
            Fallback to a request.

            Args:
                request: (todo): write your description
            """
            return HttpResponse("fallback")  # pragma: no cover

        decorator = flag_check("FLAG_DISABLED", True, fallback=fallback)
        with warnings.catch_warnings(record=True) as warning_list:
            decorator(view)

            self.assertTrue(
                any(item.category == RuntimeWarning for item in warning_list)
            )

    def test_view_fallback_same_args(self):
        """
        Decorator to skip back - in - fallback.

        Args:
            self: (todo): write your description
        """
        def view(request, extra_arg, kwarg=None):
            """
            View the given the request.

            Args:
                request: (todo): write your description
                extra_arg: (str): write your description
                kwarg: (todo): write your description
            """
            return HttpResponse("ok")  # pragma: no cover

        def fallback(request, extra_arg, kwarg=None):
            """
            Fallback to the given request.

            Args:
                request: (todo): write your description
                extra_arg: (str): write your description
                kwarg: (dict): write your description
            """
            return HttpResponse("fallback")

        decorator = flag_check("FLAG_DISABLED", True, fallback=fallback)
        decorated = decorator(view)
        response = decorated(self.request, "an extra argument", kwarg="foo")
        self.assertContains(response, "fallback")
