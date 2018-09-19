from django.test import RequestFactory, TestCase, override_settings

from flags.middleware import FlagConditionsMiddleware


@override_settings(
    MIDDLEWARE=(
        'flags.middleware.FlagConditionsMiddleware',
    )
)
class FlagConditionsMiddlewareTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = FlagConditionsMiddleware()

    def test_middleware(self):
        request = self.factory.get('/test')
        self.middleware.process_request(request)
        self.assertIn('FLAG_ENABLED', request.FLAG_CONDITIONS)
        self.assertIn('FLAG_DISABLED', request.FLAG_CONDITIONS)
        self.assertIn('DB_FLAG', request.FLAG_CONDITIONS)
