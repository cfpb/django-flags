# Wagtail-Flags

[![Build Status](https://travis-ci.org/cfpb/wagtail-flags.svg?branch=master)](https://travis-ci.org/cfpb/wagtail-flags)
[![Coverage Status](https://coveralls.io/repos/github/cfpb/wagtail-flags/badge.svg?branch=master)](https://coveralls.io/github/cfpb/wagtail-flags?branch=master)

Feature flags allow you to toggle functionality in both Django settings and the Wagtail or Django admin based on configurable conditions.

![Feature flags in the Wagtail admin](https://raw.githubusercontent.com/cfpb/wagtail-flags/master/screenshot_list.png)

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Concepts](#concepts)
- [Usage](#usage)
    - [Quickstart](#quickstart)
    - [Defining flags](#defining-flags)
    - [Using flags in code](#using-flags-in-code)
    - [Built-in conditions](#built-in-conditions)
- [API](#api)
    - [Flag state](#flag-state)
    - [Flag decorators](#flag-decorators)
    - [Flagged URLs](#flagged-urls)
    - [Django templates](#django-templates)
    - [Jinja2 templates](#jinja2-templates)
    - [Conditions](#conditions)
- [Getting help](#getting-help)
- [Getting involved](#getting-involved)
- [Licensing](#licensing)
- [Credits and references](#credits-and-references)

## Dependencies

- Django 1.8+
- Wagtail 1.10+
- Python 2.7+, 3.6+

## Installation

1. Install wagtail-flags using pip:

```shell
pip install wagtail-flags
```

2. Add `flags` as an installed app in your Django `settings.py`:

 ```python
 INSTALLED_APPS = (
     ...
     'flags',
     ...
 )
```

## Concepts

Feature flags in Wagtail-Flags are identified by simple strings that are enabled when the conditions they are associated with are met. These flags can be used to wrap code and template content that should only be used when a flag is enabled or disabled.

Conditions determine whether a flag is enabled or disabled by comparing a defined expected value of some kind with the value at the time the flag is checked. In many cases, the flag is checked during a request, and some piece of the request's metadata is what is compared. For example, a feature flag that is enabled for a specific Wagtail Site would be enabled if the request's site matches the condition's site.

## Usage

### Quickstart

To use Wagtail-Flags you first need to define the flag, use the flag, and define conditions for the flag to be enabled.

First, define the flag in Django `settings.py`:

```python
FLAGS = {
    'MY_FLAG': {}
}
```

Then use the flag in a Django template (`mytemplate.html`):

```django
{% load feature_flags %}
{% flag_enabled 'MY_FLAG' as my_flag %}

{% if my_flag %}
  <div class="flagged-banner">
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

Configure a URL for that template (`urls.py`):

```python
from django.conf.urls import url
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^/mypage$', TemplateView.as_view(template_name='mytemplate.html')),
]
```

Then in the Wagtail admin add conditions for the flag in "Settings", "Flags":

![Creating conditions in the Wagtail admin](https://raw.githubusercontent.com/cfpb/wagtail-flags/master/screenshot_create.png)


Then visiting the URL `/mypage?enable_my_flag=True` should show you the flagged `<div>` in the template.

### Adding flags

### Defining flags

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

Additional conditions can be added in the Django or Wagtail admin for any defined flag (illustrated in [Usage](#usage)). Conditions added in the Django or Wagtail admin can be changed without restarting Django, conditions defined in `settings.py` cannot. See below [for a list of built-in conditions](#built-in-conditions).

### Using flags in code

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

And Django `urls.py`:

```python
from flags.urls import flagged_url, flagged_urls

urlpatterns = [
    flagged_url('MY_FLAG', r'^an-url$', view_requiring_flag, state=True),
]
```

See the [API documentation below](#api) for more details and examples.



#### Built-in conditions

Wagtail-Flags comes with the following conditions built-in:

##### `boolean`

A simple boolean true/false intended to enable or disable a flag explicitly. The state of the flag evaluates to the value of the boolean condition.

```python
FLAGS = {'MY_FLAG': {'boolean': True}}
```

##### `user`

Allows a flag to be enabled for the username given as the condition's value.

```python
FLAGS = {'MY_FLAG': {'user': 'jane.doe'}}
```

##### `anonymous`

Allows a flag to be either enabled or disabled depending on the condition's boolean value.

```python
FLAGS = {'MY_FLAG': {'anonymous: False}}
```

##### `parameter`

Allows a flag to be enabled based on a GET parameter with the name given as the condition's value.

```python
FLAGS = {'MY_FLAG': {'parameter': 'my_flag_param'}}
```

##### `path`

Allows a flag to be enabled if the request's path matches the condition value.

```python
FLAGS = {'MY_FLAG': {'path': '/flagged/path'}}
```

##### `site`

Allows a flag to be enabled for a Wagtail site that matches the hostname and port in the condition value.

```python
FLAGS = {'MY_FLAG': {'site': 'staging.mysite.com'}}
```

##### `after date`

Allows a flag to be enabled after a given date (and time) given in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601). The time must be specified either in UTC or as an offset from UTC.

```python
FLAGS = {'MY_FLAG': {'after date': '2017-06-01T12:00Z'}}
```

## API

### Flag state

```python
from flags.state import (
    flag_state,
    flag_enabled,
    flag_disabled,
)
```

#### `flag_state(flag_name, **kwargs)`

Return the value for the flag (`True` or `False`) by passing kwargs to its conditions.

#### `flag_enabled(flag_name, **kwargs)`

Returns `True` if a flag is enabled by passing kwargs to its conditions, otherwise returns `False`.

```python
if flag_enabled('MY_FLAG', request=a_request):
	print("My feature flag is enabled")
```

#### `flag_disabled(flag_name, **kwargs)`

Returns `True` if a flag is disabled by passing kwargs to its conditions, otherwise returns `False`.

```python
if flag_disabled('MY_FLAG', request=a_request):
	print(“My feature flag is disabled”)
```

### Flag decorators

Decorators are provided for use with Django views and conditions that take a `request` argument. The default behavior is to return a 404 if a callable fallback is not given.

```python
from flags.decorators import (
    flag_check,
    flag_required,
)
```

#### `flag_check(flag_name, state, fallback=None, **kwargs)`

Check that a given flag has the given state. If the state does not match, perform the fallback.

**Note**, because flags that do not exist are taken to be `False` by default, `@flag_check('MY_FLAG', False)` and `@flag_check('MY_FLAG', None)` will both succeed if `MY_FLAG` does not exist.

```python
from flags.decorators import flag_check

@flag_check('MY_FLAG', True)
def view_requiring_flag(request):
    return HttpResponse('flag was set')

@flag_check('MY_OTHER_FLAG', False)
def view_when_flag_is_not_set(request):
    return HttpResponse('flag was set')

def other_view(request):
    return HttpResponse('flag was not set')

@flag_check('MY_FLAG_WITH_FALLBACK', True, fallback=other_view)
def view_with_fallback(request):
    return HttpResponse('flag was set')
```

#### `flag_required(flag_name, fallback_view=None, pass_if_set=True)`

Require the given flag to be enabled.

```python
from flags.decorators import flag_required

@flag_required('MY_FLAG')
def view_requiring_flag(request):
    return HttpResponse('flag was set')

def other_view(request):
    return HttpResponse('flag was not set')

@flag_required('MY_FLAG_WITH_FALLBACK', fallback_view=other_view)
def view_with_fallback(request):
    return HttpResponse('flag was set')
```

### Flagged URLs

```python
from flags.urls import flagged_url, flagged_urls
```

Flagged URLs are an alternative to [flagging views with decorators](https://github.com/cfpb/wagtail-flags#flag_checkflag_name-state-fallbacknone-kwargs).

#### `flagged_url(flag_name, regex, view, kwargs=None, name=None, state=True, fallback=None)`

Make a URL depend on the state of a feature flag. `flagged_url()` can be used in place of Django's `url()`.

The `view` and the `fallback` can both be a set of `include()`ed patterns but any matching URL patterns in the includes must match *exactly* in terms of regular expression, keyword arguments, and name, otherwise a `404` may be unexpectedly raised. 

If a `fallback` is not given the flagged url will raise a `404` if the flag state does not match the required `state`. 

```python
urlpatterns = [
    flagged_url('MY_FLAG', r'^an-url$', view_requiring_flag, state=True),
    flagged_url('MY_FLAG_WITH_FALLBACK', r'^another-url$', view_with_fallback,
                state=True, fallback=other_view)
    flagged_url('MY_FLAGGED_INCLUDE', r'^myapp$', include('myapp.urls'),
                state=True, fallback=other_view)
    flagged_url('MY_NEW_APP_FLAG', r'^mynewapp$', include('mynewapp.urls'),
                state=True, fallback=include('myoldapp.urls'))
]
```

#### `flagged_urls(flag_name, state=True, fallback=None)`

Flag multiple URLs in the same context. Returns function that can be used in place of Django's `url()` that wraps `flagged_url()`. Can take an optional fallback view that will apply to all urls.

```python
with flagged_urls('MY_FLAG') as url:
    flagged_url_patterns = [
        url(r'^an-url$', view_requiring_flag),
    ]

urlpatterns = urlpatterns + flagged_url_patterns
```

### Django templates

Wagtail-Flags provides a template tag library that can be used to evaluate flags in Django templates.

```django
{% load feature_flags %}
```

#### `flag_enabled`

Returns `True` if a flag is enabled by passing the current request to its conditions, otherwise returns `False`.

```django
{% flag_enabled 'MY_FLAG' as my_flag %}
{% if my_flag %}
  <div class="m-global-banner">
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

#### `flag_disabled`

Returns `True` if a flag is disabled by passing the current request to its conditions, otherwise returns `False`.

```django
{% flag_disabled 'MY_FLAG' as my_flag %}
{% if my_flag %}
  <div class="m-global-banner">
    I’m the result of a feature flag that is not enabled.
  </div>
{% endif %}
```

### Jinja2 templates

Wagtail-Flags provides template functions that can be added to a Jinja2 environment and subsequently used in templates.

```python
from flags.template_functions import (
    flag_enabled,
    flag_disabled
)
from jinja2 import Environment

...

env = Environment(…)
env.globals.update(
    flag_enabled=flag_enabled,
    flag_disabled=flag_disabled
)
```

#### `flag_enabled`

Returns `True` if a flag is enabled by for the given request, otherwise returns `False`.

```jinja
{% if flag_enabled('MY_FLAG', request) %}
  <div class="m-global-banner">
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

#### `flag_disabled`

Returns `True` if a flag is disabled by passing the current request to its conditions, otherwise returns `False`.
Returns `True` if a flag is disabled by for the given request, otherwise returns `False`.

```jinja
{% if flag_disabled('MY_FLAG', request) %}
  <div class="m-global-banner">
    I’m the result of a feature flag that is not enabled.
  </div>
{% endif %}
```


### Conditions

Conditions are functions that take a configured value and possible keyword arguments and determines whether the given arguments are equivalent to the value. Conditions are registered with a unique name that is exposed to users in Django settings and the Django and Wagtail admin.

```python
from flags import conditions
```

#### `conditions.register(condition_name, fn=None)`

Register a new condition, either as a decorator:

```python
from flags import conditions

@conditions.register('path')
def path_condition(path, request=None, **kwargs):
    return request.path.startswith(path)
```

Or as a function call:

```python
def path_condition(path, request=None, **kwargs):
    return request.path.startswith(path)

conditions.register('path', fn=path_condition)
```

#### `conditions.RequiredForCondition`

Exception intended to be raised when a condition is not given a keyword argument it requires for evaluation.

```python
@conditions.register('path')
def path_condition(path, request=None, **kwargs):
    if request is None:
        raise conditions.RequiredForCondition(
            "request is required for condition 'path'")

    return request.path.startswith(path)
```


## Getting help

Please add issues to the [issue tracker](https://github.com/cfpb/wagtail-flags/issues).

## Getting involved

General instructions on _how_ to contribute can be found in [CONTRIBUTING](CONTRIBUTING.md).

## Licensing
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

## Credits and references

1. Forked from [cfgov-refresh](https://github.com/cfpb/cfgov-refresh)
