from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from flags.state import flag_enabled


class EnableFlagTestCase(TestCase):
    def test_enable_flag(self):
        out = StringIO()
        self.assertFalse(flag_enabled("DB_FLAG"))
        call_command("enable_flag", "DB_FLAG", stdout=out)
        self.assertTrue(flag_enabled("DB_FLAG"))
        self.assertIn("Successfully enabled", out.getvalue())

    def test_enable_flag_non_existent_flag(self):
        with self.assertRaises(CommandError):
            call_command("enable_flag", "FLAG_DOES_NOT_EXIST")
