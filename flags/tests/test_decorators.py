import warnings
from unittest.mock import Mock

from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase

from flags.decorators import flag_check, flag_required


class FlagCheckTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.META["SERVER_NAME"] = "localhost"
        self.request.META["SERVER_PORT"] = 8000

        self.mock_view = Mock(__name__="view")
        self.view = lambda request: self.mock_view(request)

    def test_decorated_no_flag_exists(self):
        decorated = flag_check("FLAG_DOES_NOT_EXIST", True)(self.view)
        with self.assertRaises(Http404):
            decorated(self.request)
        self.assertEqual(self.mock_view.call_count, 0)

    def test_decorated_flag_disabled(self):
        decorated = flag_check("FLAG_DISABLED", True)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.mock_view.call_count, 0)

    def test_decorated_flag_enabled(self):
        def view(request):
            return HttpResponse("ok")

        decorated = flag_check("FLAG_ENABLED", True)(view)
        response = decorated(self.request)
        self.assertContains(response, "ok")

    def test_fallback_view(self):
        def fallback(request, **kwargs):
            return HttpResponse("fallback")

        decorator = flag_check("FLAG_DISABLED", True, fallback=fallback)
        decorated = decorator(self.view)
        response = decorated(self.request)
        self.assertContains(response, "fallback")

    def test_pass_if_not_set_no_flag_exists(self):
        def view(request):
            return HttpResponse("ok")

        decorated = flag_check("FLAG_DOES_NOT_EXIST", False)(view)
        response = decorated(self.request)
        self.assertContains(response, "ok")

    def test_pass_if_not_set_disabled(self):
        def view(request):
            return HttpResponse("ok")

        decorated = flag_check("FLAG_DISABLED", False)(view)
        response = decorated(self.request)
        self.assertContains(response, "ok")

    def test_pass_if_not_set_enabled(self):
        decorated = flag_check("FLAG_ENABLED", False)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.mock_view.call_count, 0)

    def test_pass_if_not_set_fallback_view(self):
        def fallback(request, **kwargs):
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
        def view(request):
            return HttpResponse("ok")

        decorated = flag_required("FLAG_ENABLED")(view)
        response = decorated(self.request)
        self.assertContains(response, "ok")

    def test_view_fallback_different_args(self):
        def view(request, extra_arg, kwarg=None):
            return HttpResponse("ok")  # pragma: no cover

        def fallback(request):
            return HttpResponse("fallback")  # pragma: no cover

        decorator = flag_check("FLAG_DISABLED", True, fallback=fallback)
        with warnings.catch_warnings(record=True) as warning_list:
            decorator(view)

            self.assertTrue(
                any(item.category is RuntimeWarning for item in warning_list)
            )

    def test_view_fallback_same_args(self):
        def view(request, extra_arg, kwarg=None):
            return HttpResponse("ok")  # pragma: no cover

        def fallback(request, extra_arg, kwarg=None):
            return HttpResponse("fallback")

        decorator = flag_check("FLAG_DISABLED", True, fallback=fallback)
        decorated = decorator(view)
        response = decorated(self.request, "an extra argument", kwarg="foo")
        self.assertContains(response, "fallback")
