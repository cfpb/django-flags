from django import forms

from flags.conditions import get_conditions
from flags.models import FlagState
from flags.sources import get_flags


class FlagStateForm(forms.ModelForm):
    name = forms.ChoiceField(
        label='Flag',
        required=True
    )
    condition = forms.ChoiceField(
        label='Condition name',
        required=True
    )
    value = forms.CharField(
        label='Expected value',
        required=True
    )
    required = forms.BooleanField(
        label='Required',
        required=False,
        help_text=('All conditions marked "required" must be met to enable '
                   'the flag'),
    )

    def __init__(self, *args, **kwargs):
        super(FlagStateForm, self).__init__(*args, **kwargs)

        self.fields['name'].choices = [
            (f, f) for f in sorted(get_flags().keys())
        ]

        self.fields['condition'].choices = [
            (c, c) for c in sorted(get_conditions())
        ]

    class Meta:
        model = FlagState
        fields = ('name', 'condition', 'value', 'required')
