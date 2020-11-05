from unittest import skipIf

from django.http import Http404, HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.urls import include, path, re_path, resolve

from flags.urls import flagged_path, flagged_re_path, flagged_re_paths


def view(request):
    """
    Displays the view.

    Args:
        request: (todo): write your description
    """
    return HttpResponse("view")


def fallback(request):
    """
    Fallback to a request.

    Args:
        request: (todo): write your description
    """
    return HttpResponse("fallback")


extra_patterns = [
    re_path(r"^included-url$", view),
    re_path(r"^included-url-with-fallback$", view),
]
fallback_patterns = [
    re_path(r"^included-url-with-fallback$", fallback),
    re_path(r"^other-included-url$", fallback),
]

urlpatterns = [
    flagged_re_path(
        "FLAGGED_URL",
        r"^url-true-no-fallback$",
        view,
        name="some-view",
        state=True,
    ),
    flagged_re_path(
        "FLAGGED_URL",
        r"^url-false-no-fallback$",
        view,
        name="some-view",
        state=False,
    ),
    flagged_re_path(
        "FLAGGED_URL",
        r"^url-true-fallback$",
        view,
        name="some-view",
        state=True,
        fallback=fallback,
    ),
    flagged_re_path(
        "FLAGGED_URL",
        r"^url-false-fallback$",
        view,
        name="some-view",
        state=False,
        fallback=fallback,
    ),
    flagged_re_path(
        "FLAGGED_URL", r"^include/", include(extra_patterns), state=True
    ),
    flagged_re_path(
        "FLAGGED_URL",
        r"^include-false/",
        include(extra_patterns),
        state=False,
    ),
    flagged_re_path(
        "FLAGGED_URL",
        r"^include-fallback/",
        include(extra_patterns),
        state=True,
        fallback=fallback,
    ),
    flagged_re_path(
        "FLAGGED_URL",
        r"^include-false-fallback/",
        include(extra_patterns),
        state=True,
        fallback=fallback,
    ),
    flagged_re_path(
        "FLAGGED_URL",
        r"^include-fallback-include/",
        include(extra_patterns),
        state=True,
        fallback=include(fallback_patterns),
    ),
]

with flagged_re_paths("FLAGGED_URL") as re_path:
    flagged_patterns_true_no_fallback = [
        re_path(r"^patterns-true-no-fallback$", view, name="some-view"),
    ]
urlpatterns = urlpatterns + flagged_patterns_true_no_fallback

with flagged_re_paths("FLAGGED_URL", state=False) as re_path:
    flagged_patterns_false_no_fallback = [
        re_path(r"^patterns-false-no-fallback$", view, name="some-view"),
    ]
urlpatterns = urlpatterns + flagged_patterns_false_no_fallback

with flagged_re_paths("FLAGGED_URL", fallback=fallback) as re_path:
    flagged_patterns_true_fallback = [
        re_path(r"^patterns-true-fallback$", view, name="some-view"),
    ]
urlpatterns = urlpatterns + flagged_patterns_true_fallback

path_patterns = [
    flagged_path(
        "FLAGGED_URL",
        "path-true-no-fallback",
        view,
        name="some-view",
        state=True,
    ),
]
urlpatterns = urlpatterns + path_patterns


@override_settings(ROOT_URLCONF=__name__)
class FlagCheckTestCase(TestCase):
    def setUp(self):
        """
        Sets the flag.

        Args:
            self: (todo): write your description
        """
        self.flag_name = "FLAGGED_URL"
        self.factory = RequestFactory()

    def get_url_response(self, url):
        """
        Get the url for the given url.

        Args:
            self: (todo): write your description
            url: (str): write your description
        """
        request = self.factory.get(url)
        resolved_view, args, kwargs = resolve(url)
        response = resolved_view(request)
        return response

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_url_true_no_fallback(self):
        """
        Flagged test url test url test url.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/url-true-no-fallback")
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_true_no_fallback_false(self):
        """
        Test if the test.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(Http404):
            self.get_url_response("/url-true-no-fallback")

    @skipIf(not path, "Skipping test for Django 2.0 path() patterns")
    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_path_true_no_fallback(self):  # pragma: no cover
        """
        Flagged test path to test for the test test.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/path-true-no-fallback")
        self.assertContains(response, "view")

    @skipIf(not path, "Skipping test for Django 2.0 path() patterns")
    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_path_true_no_fallback_false(self):  # pragma: no cover
        """
        Test if the test path.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(Http404):
            self.get_url_response("/path-true-no-fallback")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_false_no_fallback(self):
        """
        Flagged url test url test.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/url-false-no-fallback")
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_url_false_no_fallback_true(self):
        """
        Test if the test test is closed.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(Http404):
            self.get_url_response("/url-false-no-fallback")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_url_true_fallback(self):
        """
        Flagged test url test is true.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/url-true-fallback")
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_true_fallback_false(self):
        """
        Test if the test is_url.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/url-true-fallback")
        self.assertContains(response, "fallback")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_false_fallback(self):
        """
        Flagged test url fallback.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/url-false-fallback")
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_url_false_fallback_false(self):
        """
        Flagged url test test url.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/url-false-fallback")
        self.assertContains(response, "fallback")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_url_true_include_true(self):
        """
        Flagged test url true is true.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/include/included-url")
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_true_include_false(self):
        """
        Test if the url true if the test is true.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(Http404):
            self.get_url_response("/include/included-url")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_false_include(self):
        """
        Flagged url test test url.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/include-false/included-url")
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_url_false_include_true(self):
        """
        Test if the test url is true.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(Http404):
            self.get_url_response("/include-false/included-url")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_include_fallback(self):
        """
        Flagged test url test test test url.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/include-fallback/included-url")
        self.assertContains(response, "fallback")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_url_true_include_fallback_include(self):
        """
        Test if the test url test url_true

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response(
            "/include-fallback-include/included-url-with-fallback"
        )
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_false_include_fallback_include(self):
        """
        Test if the test test url.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response(
            "/include-fallback-include/included-url-with-fallback"
        )
        self.assertContains(response, "fallback")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_false_include_fallback_none(self):
        """
        Flagged url test for the test.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(Http404):
            self.get_url_response("/include-fallback-include/included-url")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_url_true_include_fallback_include_nonmatching_url(self):
        """
        Test if url url url url.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(Http404):
            self.get_url_response(
                "/include-fallback-include/other-included-url"
            )

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_url_false_include_fallback_include_nonmatching_url(self):
        """
        Flagged url url url url.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response(
            "/include-fallback-include/other-included-url"
        )
        self.assertContains(response, "fallback")

    def test_flagged_url_not_callable(self):
        """
        Test if the test test url.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(TypeError):
            flagged_re_path("MY_FLAG", r"^my_url/$", "string")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_urls_cm_true_no_fallback(self):
        """
        Flagged test urls.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/patterns-true-no-fallback")
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_urls_cm_true_no_fallback_false(self):
        """
        Test if the test urls exist.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(Http404):
            self.get_url_response("/patterns-true-no-fallback")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_urls_cm_false_no_fallback(self):
        """
        Flagged test test test urls.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/patterns-false-no-fallback")
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_urls_cm_false_no_fallback_true(self):
        """
        Flagged test test test test test_true.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(Http404):
            self.get_url_response("/patterns-false-no-fallback")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", True)]})
    def test_flagged_urls_cm_true_fallback(self):
        """
        Flagged test urls.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/patterns-true-fallback")
        self.assertContains(response, "view")

    @override_settings(FLAGS={"FLAGGED_URL": [("boolean", False)]})
    def test_flagged_urls_cm_true_fallback_false(self):
        """
        Flagged test urls.

        Args:
            self: (todo): write your description
        """
        response = self.get_url_response("/patterns-true-fallback")
        self.assertContains(response, "fallback")
