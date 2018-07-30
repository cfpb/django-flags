# Usage guide

## Defining flags

Flags are defined in Django settings with the conditions in which they are enabled.

```python
FLAGS = {
  'FLAG_WITH_EMPTY_CONDITIONS': {}
  'MY_FLAG': {
    'condition name': 'value flag is expected to match to be enabled',
    'user': 'lady.liberty'
  }
}
```

The set of conditions can be none (flag will never be enabled), one (only condition that has to be met for the flag to be enabled), or many (all have to be met for the flag to be enabled).

Additional conditions can be added in the Django admin for any defined flag (illustrated in [Usage](#usage)). Conditions added in the Django admin can be changed without restarting Django, conditions defined in `settings.py` cannot. See below [for a list of built-in conditions](#built-in-conditions).

## Using flags in code

Flags can be used in Python code:

```python
from flags.state import flag_enabled

if flag_enabled('MY_FLAG', request=a_request):
    print("My feature flag is enabled")	
```

Django templates:

```django
{% load feature_flags %}
{% flag_enabled 'MY_FLAG' as my_flag %}
{% if my_flag %}
  <div>
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

Jinja2 templates (after [adding `flag_enabled` to the Jinja2 environment](#jinja2-templates)):

```jinja
{% if flag_enabled('MY_FLAG', request) %}
  <div>
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

Django 2.0 `urls.py`:

```python
from flags.urls import flagged_path

urlpatterns = [
    flagged_path('MY_FLAG', 'a-url/', view_requiring_flag, state=True),
]
```

And Django 1.x `urls.py`:

```python
from flags.urls import flagged_url

urlpatterns = [
    flagged_url('MY_FLAG', r'^a-url$', view_requiring_flag, state=True),
]
```

See the [API documentation below](#api) for more details and examples.
