import warnings

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase, override_settings
from django.views.generic import View

from flags.views import FlaggedViewMixin


class TestView(FlaggedViewMixin, View):
    def get(self, request, *args, **kwargs):
        """
        Handles the http get request.

        Args:
            self: (todo): write your description
            request: (todo): write your description
        """
        return HttpResponse("ok")


class FlaggedViewMixinTestCase(TestCase):
    def setUp(self):
        """
        Sets the flag.

        Args:
            self: (todo): write your description
        """
        self.flag_name = "FLAGGED_VIEW_MIXIN"

    def request(self, path="/"):
        """
        Make a request. request.

        Args:
            self: (todo): write your description
            path: (str): write your description
        """
        request = HttpRequest()

        request.method = "GET"
        request.path = path
        request.META["SERVER_NAME"] = "localhost"
        request.META["SERVER_PORT"] = 8000

        return request

    def test_no_flag_key_raises_improperly_configured(self):
        """
        Set the flag flag flag flag flag flag flag.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ImproperlyConfigured):
            TestView.as_view()

    def test_no_flag_acts_as_disabled(self):
        """
        Enables or disassociates the flag.

        Args:
            self: (todo): write your description
        """
        view = TestView.as_view(flag_name=self.flag_name)
        self.assertRaises(Http404, view, self.request())

    @override_settings(FLAGS={"FLAGGED_VIEW_MIXIN": [("boolean", True)]})
    def test_flag_set_view_enabled(self):
        """
        This method is set_flag_set_enabled

        Args:
            self: (todo): write your description
        """
        view = TestView.as_view(flag_name=self.flag_name)
        self.assertEqual(view(self.request()).status_code, 200)

    @override_settings(FLAGS={"FLAGGED_VIEW_MIXIN": [("boolean", False)]})
    def test_flag_set_view_disabled(self):
        """
        Sets the test flag to be set.

        Args:
            self: (todo): write your description
        """
        view = TestView.as_view(flag_name=self.flag_name)
        self.assertRaises(Http404, view, self.request())

    def test_fallback_view_function_disabled(self):
        """
        Decorator for fall back to the test function.

        Args:
            self: (todo): write your description
        """
        def test_view_function(request, *args, **kwargs):
            """
            Decorator for views that the request.

            Args:
                request: (todo): write your description
            """
            return HttpResponse("fallback fn")

        view = TestView.as_view(
            flag_name=self.flag_name,
            state=True,
            fallback=test_view_function,
        )

        response = view(self.request())
        self.assertContains(response, "fallback fn")

    @override_settings(FLAGS={"FLAGGED_VIEW_MIXIN": [("boolean", True)]})
    def test_fallback_view_function_enabled(self):
        """
        Decorator to ensure that the test_view.

        Args:
            self: (todo): write your description
        """
        fallback = lambda request, *args, **kwargs: HttpResponse("fallback fn")
        view = TestView.as_view(
            flag_name=self.flag_name, state=True, fallback=fallback
        )

        response = view(self.request())
        self.assertContains(response, "ok")

    def test_fallback_class_based_view(self):
        """
        Fallback for a fallback class.

        Args:
            self: (todo): write your description
        """
        class OtherTestView(View):
            def get(self, request, *args, **kwargs):
                """
                Handles the http get request.

                Args:
                    self: (todo): write your description
                    request: (todo): write your description
                """
                return HttpResponse("fallback cbv")

        view = TestView.as_view(
            flag_name=self.flag_name,
            state=True,
            fallback=OtherTestView.as_view(),
        )

        response = view(self.request())
        self.assertContains(response, "fallback cbv")

    @override_settings(FLAGS={"FLAGGED_VIEW_MIXIN": [("boolean", True)]})
    def test_deprecated_condition_attr(self):
        """
        Test for deprecated.

        Args:
            self: (todo): write your description
        """
        with warnings.catch_warnings(record=True) as warning_list:
            view = TestView.as_view(flag_name=self.flag_name, condition=True)
            response = view(self.request())

            self.assertTrue(
                any(item.category == FutureWarning for item in warning_list)
            )

            self.assertContains(response, "ok")
