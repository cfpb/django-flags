from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from flags.models import FlagState
from flags.state import flag_disabled


class disableFlagTestCase(TestCase):
    def test_disable_flag(self):
        FlagState.objects.create(
            name="DB_FLAG", condition="boolean", value="True"
        )
        out = StringIO()
        self.assertFalse(flag_disabled("DB_FLAG"))
        call_command("disable_flag", "DB_FLAG", stdout=out)
        self.assertTrue(flag_disabled("DB_FLAG"))
        self.assertIn("Successfully disabled", out.getvalue())

    def test_disable_flag_non_existent_flag(self):
        with self.assertRaises(CommandError):
            call_command("disable_flag", "FLAG_DOES_NOT_EXIST")
