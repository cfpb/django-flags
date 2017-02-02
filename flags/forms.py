from django import forms
from django.core import validators

from .models import Flag, FlagState


validate_flag = validators.RegexValidator(
    r'^[-a-zA-Z0-9_]+\Z',
    "Enter a valid flag consisting of letters, numbers, or underscores.",
    'invalid'
)


class SelectSiteForm(forms.Form):
    site_id = forms.IntegerField()


class FeatureFlagForm(forms.ModelForm):
    key = forms.CharField(validators=[validate_flag])

    class Meta:
        model = Flag
        fields = ('key', )


class FlagStateForm(forms.ModelForm):
    class Meta:
        model = FlagState
        fields = ('flag', 'enabled', 'site')
        widgets = {
            'flag': forms.widgets.HiddenInput(),
            'site': forms.widgets.HiddenInput(),
        }
