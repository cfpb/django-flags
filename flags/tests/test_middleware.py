from django.test import (
    RequestFactory,
    SimpleTestCase,
    TestCase,
    override_settings,
)

from flags.middleware import FlagConditionsMiddleware
from flags.state import flag_state


@override_settings(
    FLAG_SOURCES=('flags.sources.SettingsFlagsSource', )
)
class FlagConditionsMiddlewareTestCase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = FlagConditionsMiddleware()

    def test_requests_without_middleware_attribute_is_undefined(self):
        request = self.factory.get('/test')
        self.assertFalse(hasattr(
            request,
            FlagConditionsMiddleware.request_attribute
        ))

    def test_middleware_defines_attribute(self):
        request = self.factory.get('/test')
        self.middleware.process_request(request)
        self.assertTrue(hasattr(
            request,
            FlagConditionsMiddleware.request_attribute
        ))

    def test_middleware_sets_attribute_with_flags(self):
        request = self.factory.get('/test')
        self.middleware.process_request(request)
        flags = getattr(request, FlagConditionsMiddleware.request_attribute)
        self.assertIn('FLAG_ENABLED', flags)
        self.assertIn('FLAG_DISABLED', flags)
        self.assertIn('DB_FLAG', flags)


class FlagConditionsMiddlewareStateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = FlagConditionsMiddleware()

    def test_flag_state_uses_cached_request_flags(self):
        request = self.factory.get('/test')
        self.middleware.process_request(request)
        with override_settings(FLAGS={}):
            self.assertTrue(flag_state('FLAG_ENABLED', request=request))

    def test_flag_state_without_middleware_has_no_cached_request_flags(self):
        request = self.factory.get('/test')
        with override_settings(FLAGS={}):
            self.assertFalse(flag_state('FLAG_ENABLED', request=request))
