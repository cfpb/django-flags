from django import forms

from flags.conditions import get_conditions
from flags.models import FlagState
from flags.settings import get_flags

FLAGS_CHOICES = [(flag, flag) for flag in get_flags().keys()]
CONDITIONS_CHOICES = [(c, c) for c in get_conditions()]


class FlagStateForm(forms.ModelForm):
    name = forms.ChoiceField(choices=FLAGS_CHOICES,
                             label="Flag",
                             required=True)
    condition = forms.ChoiceField(choices=CONDITIONS_CHOICES,
                                  label="Is enabled when",
                                  required=True)
    value = forms.CharField(label="Is", required=True)

    class Meta:
        model = FlagState
        fields = ('name', 'condition', 'value')
