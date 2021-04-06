from django.apps import AppConfig


class TestAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "flags.tests.testapp"
