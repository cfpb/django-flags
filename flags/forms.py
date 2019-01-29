from django import forms

from flags.conditions import get_conditions
from flags.models import FlagState
from flags.sources import get_flags


class FlagStateForm(forms.ModelForm):
    name = forms.ChoiceField(
        label="Flag",
        required=True
    )
    condition = forms.ChoiceField(
        label="Is enabled when",
        required=True
    )
    value = forms.CharField(
        label="Is",
        required=True,
        widget=forms.Textarea(
            attrs={
                'rows': 2,
                'cols': 40,
            }
        )
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
        fields = ('name', 'condition', 'value')
