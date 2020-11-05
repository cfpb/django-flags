from django.contrib import admin
from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import re_path


urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
]


@override_settings(
    ROOT_URLCONF=__name__,
)
class FlagsAdminTestCase(TestCase):
    def setUp(self):
        """
        Set up a new login.

        Args:
            self: (todo): write your description
        """
        self.client = Client()
        self.user = User.objects.create_superuser(
            "test", "test@email.com", "testing"
        )
        self.client.login(username="test", password="testing")

    def test_flags_admin(self):
        """
        Check the status of the test status.

        Args:
            self: (todo): write your description
        """
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
