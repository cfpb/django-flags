from django.conf.urls import url, include
from django.core.urlresolvers import resolve
from django.http import HttpResponse, Http404
from django.test import TestCase, RequestFactory, override_settings

from flags.urls import flagged_url, flagged_urls


def view(request):
    return HttpResponse('view')


def fallback(request):
    return HttpResponse('fallback')


extra_patterns = [
    url(r'^included-url$', view),
    url(r'^included-url-with-fallback$', view),
]
fallback_patterns = [
    url(r'^included-url-with-fallback$', fallback),
    url(r'^other-included-url$', fallback),
]

urlpatterns = [
    flagged_url('FLAGGED_URL', r'^url-true-no-fallback$', view,
                name='some-view', state=True),
    flagged_url('FLAGGED_URL', r'^url-false-no-fallback$', view,
                name='some-view', state=False),
    flagged_url('FLAGGED_URL', r'^url-true-fallback$', view,
                name='some-view', state=True, fallback=fallback),
    flagged_url('FLAGGED_URL', r'^url-false-fallback$', view,
                name='some-view', state=False, fallback=fallback),

    flagged_url('FLAGGED_URL', r'^include/', include(extra_patterns),
                state=True),
    flagged_url('FLAGGED_URL', r'^include-false/', include(extra_patterns),
                state=False),
    flagged_url('FLAGGED_URL', r'^include-fallback/', include(extra_patterns),
                state=True, fallback=fallback),
    flagged_url('FLAGGED_URL', r'^include-false-fallback/',
                include(extra_patterns), state=True, fallback=fallback),
    flagged_url('FLAGGED_URL', r'^include-fallback-include/',
                include(extra_patterns),
                state=True, fallback=include(fallback_patterns)),
]

with flagged_urls('FLAGGED_URL') as url:
    flagged_patterns_true_no_fallback = [
        url(r'^patterns-true-no-fallback$', view, name='some-view'),
    ]
urlpatterns = urlpatterns + flagged_patterns_true_no_fallback

with flagged_urls('FLAGGED_URL', state=False) as url:
    flagged_patterns_false_no_fallback = [
        url(r'^patterns-false-no-fallback$', view, name='some-view'),
    ]
urlpatterns = urlpatterns + flagged_patterns_false_no_fallback

with flagged_urls('FLAGGED_URL', fallback=fallback) as url:
    flagged_patterns_true_fallback = [
        url(r'^patterns-true-fallback$', view, name='some-view'),
    ]
urlpatterns = urlpatterns + flagged_patterns_true_fallback


@override_settings(
    ROOT_URLCONF=__name__,
)
class FlagCheckTestCase(TestCase):
    def setUp(self):
        self.flag_name = 'FLAGGED_URL'
        self.factory = RequestFactory()

    def get_url_response(self, url):
        request = self.factory.get(url)
        resolved_view, args, kwargs = resolve(url)
        response = resolved_view(request)
        return response

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_url_true_no_fallback(self):
        response = self.get_url_response('/url-true-no-fallback')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_true_no_fallback_false(self):
        with self.assertRaises(Http404):
            self.get_url_response('/url-true-no-fallback')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_false_no_fallback(self):
        response = self.get_url_response('/url-false-no-fallback')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_url_false_no_fallback_true(self):
        with self.assertRaises(Http404):
            self.get_url_response('/url-false-no-fallback')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_url_true_fallback(self):
        response = self.get_url_response('/url-true-fallback')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_true_fallback_false(self):
        response = self.get_url_response('/url-true-fallback')
        self.assertContains(response, 'fallback')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_false_fallback(self):
        response = self.get_url_response('/url-false-fallback')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_url_false_fallback_false(self):
        response = self.get_url_response('/url-false-fallback')
        self.assertContains(response, 'fallback')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_url_true_include_true(self):
        response = self.get_url_response('/include/included-url')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_true_include_false(self):
        with self.assertRaises(Http404):
            self.get_url_response('/include/included-url')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_false_include(self):
        response = self.get_url_response('/include-false/included-url')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_url_false_include_true(self):
        with self.assertRaises(Http404):
            self.get_url_response('/include-false/included-url')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_include_fallback(self):
        response = self.get_url_response('/include-fallback/included-url')
        self.assertContains(response, 'fallback')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_url_true_include_fallback_include(self):
        response = self.get_url_response(
            '/include-fallback-include/included-url-with-fallback')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_false_include_fallback_include(self):
        response = self.get_url_response(
            '/include-fallback-include/included-url-with-fallback')
        self.assertContains(response, 'fallback')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_false_include_fallback_none(self):
        with self.assertRaises(Http404):
            self.get_url_response(
                '/include-fallback-include/included-url')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_url_true_include_fallback_include_nonmatching_url(self):
        with self.assertRaises(Http404):
            self.get_url_response(
                '/include-fallback-include/other-included-url')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_url_false_include_fallback_include_nonmatching_url(self):
        response = self.get_url_response(
            '/include-fallback-include/other-included-url')
        self.assertContains(response, 'fallback')

    def test_flagged_url_not_callable(self):
        with self.assertRaises(TypeError):
            flagged_url('MY_FLAG', r'^my_url/$', 'string')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_urls_cm_true_no_fallback(self):
        response = self.get_url_response('/patterns-true-no-fallback')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_urls_cm_true_no_fallback_false(self):
        with self.assertRaises(Http404):
            self.get_url_response('/patterns-true-no-fallback')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_urls_cm_false_no_fallback(self):
        response = self.get_url_response('/patterns-false-no-fallback')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_urls_cm_false_no_fallback_true(self):
        with self.assertRaises(Http404):
            self.get_url_response('/patterns-false-no-fallback')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': True}})
    def test_flagged_urls_cm_true_fallback(self):
        response = self.get_url_response('/patterns-true-fallback')
        self.assertContains(response, 'view')

    @override_settings(FLAGS={'FLAGGED_URL': {'boolean': False}})
    def test_flagged_urls_cm_true_fallback_false(self):
        response = self.get_url_response('/patterns-true-fallback')
        self.assertContains(response, 'fallback')
