from django.test import TestCase

from flags.forms import FlagStateForm


class FormTestCase(TestCase):

    def test_valid_data(self):
        form = FlagStateForm({
            'name': 'FLAG_ENABLED',
            'condition': 'boolean',
            'value': 'True'
        })
        self.assertTrue(form.is_valid())
        state = form.save()
        self.assertEqual(state.name, 'FLAG_ENABLED')
        self.assertEqual(state.condition, 'boolean')
        self.assertEqual(state.value, 'True')

    def test_blank_data(self):
        form = FlagStateForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'condition': ['This field is required.'],
            'value': ['This field is required.'],
        })
