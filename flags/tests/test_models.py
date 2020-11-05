from django.test import TestCase

from flags.models import FlagState


class FlagStateTestCase(TestCase):
    def test_flag_str(self):
        """
        Test if the state of a string.

        Args:
            self: (todo): write your description
        """
        state = FlagState.objects.create(
            name="MY_FLAG", condition="boolean", value="True"
        )
        self.assertEqual(str(state), "MY_FLAG is enabled when boolean is True")

    def test_flag_str_required(self):
        """
        Assertools. flag_strategy.

        Args:
            self: (todo): write your description
        """
        state = FlagState.objects.create(
            name="MY_FLAG", condition="boolean", value="True", required=True
        )
        self.assertEqual(
            str(state), "MY_FLAG is enabled when boolean is True (required)"
        )
