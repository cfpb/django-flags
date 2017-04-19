try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase

from flags.decorators import flag_check, flag_required


class FlagCheckTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.META['SERVER_NAME'] = 'localhost'
        self.request.META['SERVER_PORT'] = 8000

        self.view = Mock(__name__='view')

    def test_decorated_no_flag_exists(self):
        decorated = flag_check('FLAG_DOES_NOT_EXIST', True)(self.view)
        with self.assertRaises(Http404):
            decorated(self.request)
        self.assertEqual(self.view.call_count, 0)

    def test_decorated_flag_disabled(self):
        decorated = flag_check('FLAG_DISABLED', True)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.view.call_count, 0)

    def test_decorated_flag_enabled(self):
        def view(request):
            return HttpResponse('ok')

        decorated = flag_check('FLAG_ENABLED', True)(view)
        response = decorated(self.request)
        self.assertContains(response, 'ok')

    def test_fallback_view(self):
        def fallback(request):
            return HttpResponse('fallback')

        decorator = flag_check('FLAG_DISABLED', True, fallback=fallback)
        decorated = decorator(self.view)
        response = decorated(self.request)
        self.assertContains(response, 'fallback')

    def test_pass_if_not_set_no_flag_exists(self):
        def view(request):
            return HttpResponse('ok')

        decorated = flag_check('FLAG_DOES_NOT_EXIST', False)(view)
        response = decorated(self.request)
        self.assertContains(response, 'ok')

    def test_pass_if_not_set_disabled(self):
        def view(request):
            return HttpResponse('ok')

        decorated = flag_check('FLAG_DISABLED', False)(view)
        response = decorated(self.request)
        self.assertContains(response, 'ok')

    def test_pass_if_not_set_enabled(self):
        decorated = flag_check('FLAG_ENABLED', False)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.view.call_count, 0)

    def test_pass_if_not_set_fallback_view(self):
        def fallback(request):
            return HttpResponse('fallback')

        decorator = flag_check(
            'FLAG_ENABLED',
            False,
            fallback=fallback,
        )

        decorated = decorator(self.view)
        response = decorated(self.request)
        self.assertContains(response, 'fallback')

    def test_flag_required(self):
        def view(request):
            return HttpResponse('ok')

        decorated = flag_required('FLAG_ENABLED')(view)
        response = decorated(self.request)
        self.assertContains(response, 'ok')
