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

Additional conditions can be added in the Django admin for any defined flag (illustrated in [Quickstart](../#quickstart)). Conditions added in the Django admin can be changed without restarting Django, conditions defined in `settings.py` cannot. See [the list of built-in conditions](conditions).

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

Jinja2 templates (after [adding `flag_enabled` to the Jinja2 environment](api/jinja2/)):

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

See the [API reference](/api/state) for more details and examples.

## Defining flags

### `FLAGS`

Default: `{}`


## Caching flag conditions

It is possible that a request cycle could check numerous flags, or check a single flag multiple times. Because flag conditions created in the Django admin are stored in the database, this can result in multiple identical database queries. The default cache key is `flags`. To enable caching of flag conditions with a cache key of `flags_conditions`:

```python
FLAGS_CACHE_CONDITIONS = True
FLAGS_CACHE_KEY = 'flags_conditions'
```

See the [Settings reference](settings/) for more details.
