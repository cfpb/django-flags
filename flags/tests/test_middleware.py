import warnings

from django.test import SimpleTestCase

from flags.middleware import FlagConditionsMiddleware


class FlagConditionsMiddlewareTests(SimpleTestCase):
    def test_middleware_raises_warning(self):
        with warnings.catch_warnings(record=True) as warning_list:
            FlagConditionsMiddleware(None)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[0].category, FutureWarning)
