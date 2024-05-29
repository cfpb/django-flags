# Usage guide

## Defining flags

Flags are defined in Django settings with the conditions in which they are enabled.

```python
FLAGS = {
    'FLAG_WITH_EMPTY_CONDITIONS': [],
    'FLAG_WITH_ANY_CONDITIONS': [
        {'condition': 'condition name', 'value': 'expected value to be enabled'},
        {'condition': 'user', 'value': 'lady.liberty'},
    ],
    'FLAG_WITH_REQUIRED_CONDITIONS': [
        {'condition': 'user', 'value': 'lady.liberty'},
        {'condition': 'path matches', 'value': r'^/liberty/island', 'required': True},
    ]
}
```

The set of conditions can be empty (flag will never be enabled), have one or more conditions that are not required (any of those conditions can be met for the flag to be enabled), or one or more required conditions (all required conditions have to be met for the flag to be enabled).

Additional conditions can be added in the Django admin for any defined flag (illustrated in [Quickstart](../#quickstart)). Conditions added in the Django admin can be changed without restarting Django, conditions defined in `settings.py` cannot. See [the list of built-in conditions](../conditions/).

## Using flags in code

Flags can be used in Python code:

```python
from flags.state import flag_enabled

if flag_enabled('FLAG_WITH_ANY_CONDITIONS', request=a_request):
    print("My feature flag is enabled")	
```

In Django templates:

```django
{% load feature_flags %}
{% flag_enabled 'FLAG_WITH_ANY_CONDITIONS' as my_flag %}
{% if my_flag %}
  <div>
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

In Jinja2 templates (after [adding `flag_enabled` to the Jinja2 environment](../api/jinja2/)):

```jinja
{% if flag_enabled('FLAG_WITH_ANY_CONDITIONS', request) %}
  <div>
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

In `urls.py`:

```python
from flags.urls import flagged_path

urlpatterns = [
    flagged_path('FLAG_WITH_REQUIRED_CONDITIONS', 'a-url/', view_requiring_flag, state=True),
]
```

## Testing with flags

A test case that covers both values of the flag may look like this:

```python
from django.test import TestCase, override_settings

class FlaggedCodeTestCase(TestCase):
    @override_settings(FLAGS={"MY_FLAG": [("boolean", True)]})
    def test_flag_enabled(self):
        # Do the thing that requires the flag to be enabled

    @override_settings(FLAGS={"MY_FLAG": [("boolean", False)]})
    def test_flag_disabled(self):
        # Do the thing that requires the flag to be disabled
```


See the [API reference](/django-flags/api/state) for more details and examples.
