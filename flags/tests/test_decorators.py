try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase

from flags.decorators import flag_check
from flags.models import Flag


class FlagCheckTestCase(TestCase):
    def setUp(self):
        self.flag_name = 'FLAG_REQUIRED_TEST_CASE'

        self.request = HttpRequest()
        self.request.META['SERVER_NAME'] = 'localhost'
        self.request.META['SERVER_PORT'] = 8000

        self.view = Mock(__name__='view')

    def test_decorated_no_flag_exists(self):
        decorated = flag_check(self.flag_name, True)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.view.call_count, 0)

    def test_decorated_flag_disabled(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=False)
        decorated = flag_check(self.flag_name, True)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.view.call_count, 0)

    def test_decorated_flag_enabled(self):
        def view(request):
            return HttpResponse('ok')

        Flag.objects.create(key=self.flag_name, enabled_by_default=True)
        decorated = flag_check(self.flag_name, True)(view)
        response = decorated(self.request)
        if isinstance(response.content, str):
            content = response.content
        else:
            content = bytes.decode(response.content)
        self.assertEqual(content, 'ok')

    def test_fallback_view(self):
        def fallback(request):
            return HttpResponse('fallback')

        decorator = flag_check(self.flag_name, True, fallback=fallback)
        decorated = decorator(self.view)
        response = decorated(self.request)
        if isinstance(response.content, str):
            content = response.content
        else:
            content = bytes.decode(response.content)
        self.assertEqual(content, 'fallback')

    def test_pass_if_not_set_no_flag_exists(self):
        def view(request):
            return HttpResponse('ok')

        decorated = flag_check(self.flag_name, False)(view)
        response = decorated(self.request)
        if isinstance(response.content, str):
            content = response.content
        else:
            content = bytes.decode(response.content)
        self.assertEqual(content, 'ok')

    def test_pass_if_not_set_disabled(self):
        def view(request):
            return HttpResponse('ok')

        Flag.objects.create(key=self.flag_name, enabled_by_default=False)
        decorated = flag_check(self.flag_name, False)(view)
        response = decorated(self.request)
        if isinstance(response.content, str):
            content = response.content
        else:
            content = bytes.decode(response.content)
        self.assertEqual(content, 'ok')

    def test_pass_if_not_set_enabled(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=True)
        decorated = flag_check(self.flag_name, False)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.view.call_count, 0)

    def test_pass_if_not_set_fallback_view(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=True)

        def fallback(request):
            return HttpResponse('fallback')

        decorator = flag_check(
            self.flag_name,
            False,
            fallback=fallback,
        )

        decorated = decorator(self.view)
        response = decorated(self.request)
        if isinstance(response.content, str):
            content = response.content
        else:
            content = bytes.decode(response.content)
        self.assertEqual(content, 'fallback')
