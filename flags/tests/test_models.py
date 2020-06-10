from django.test import TestCase

from flags.models import FlagMetadata, FlagState


class FlagStateTestCase(TestCase):
    def test_flag_str(self):
        state = FlagState.objects.create(
            name="MY_FLAG", condition="boolean", value="True"
        )
        self.assertEqual(str(state), "MY_FLAG is enabled when boolean is True")

    def test_flag_str_required(self):
        state = FlagState.objects.create(
            name="MY_FLAG", condition="boolean", value="True", required=True
        )
        self.assertEqual(
            str(state), "MY_FLAG is enabled when boolean is True (required)"
        )


class FlagMetadataTestCase(TestCase):
    def test_flag_str(self):
        metadata = FlagMetadata.objects.create(
            name="MY_FLAG", key="help_text", value="enable a cool thing"
        )
        self.assertEqual(
            str(metadata), "MY_FLAG (help_text: enable a cool thing)"
        )
