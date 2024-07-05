from django import forms

from flags.conditions import get_condition, get_conditions
from flags.models import FlagState
from flags.sources import get_flags


class FlagStateForm(forms.ModelForm):
    name = forms.ChoiceField(label="Flag", required=True)
    condition = forms.ChoiceField(label="Condition name", required=True)
    value = forms.CharField(label="Expected value", required=True)
    required = forms.BooleanField(
        label="Required",
        required=False,
        help_text=(
            'All conditions marked "required" must be met to enable '
            "the flag"
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].choices = [
            (f, f) for f in sorted(get_flags().keys())
        ]

        self.fields["condition"].choices = [
            (c, c) for c in sorted(get_conditions())
        ]

    def clean_value(self):
        condition_name = self.cleaned_data.get("condition")
        value = self.cleaned_data.get("value")
        condition = get_condition(condition_name)
        validator = condition.validate

        if validator is not None:
            try:
                validator(value)
            except Exception as err:
                raise forms.ValidationError(err) from err

        return value

    class Meta:
        model = FlagState
        fields = ("name", "condition", "value", "required")
