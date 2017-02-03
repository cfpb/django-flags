# Wagtail-Flags

[![Build Status](https://travis-ci.org/cfpb/wagtail-flags.svg?branch=master)](https://travis-ci.org/cfpb/wagtail-flags)
[![Coverage Status](https://coveralls.io/repos/github/cfpb/wagtail-flags/badge.svg?branch=master)](https://coveralls.io/github/cfpb/wagtail-flags?branch=master)

Feature flags allow you to toggle functionality without multiple deployments. Wagtail-Flags lets you use feature flags that are set in the Wagtail admin.

![Feature flags in the Wagtail admin](screenshot.png)


## Dependencies

- Django 1.8+
- Wagtail 1.7+
- Python 2.7+, 3.5+
 

## Installation

1. Install wagtail-flags using pip:

   ```shell
pip install git+https://github.com/cfpb/wagtail-flags.git
```

2. Add `flags` as an installed app in your Django `settings.py`:

   ```python
 INSTALLED_APPS = (
     ...
     'flags',
     ...
 )
```


## Usage

Feature flags in Wagtail-Flags are stored in the database, exposed to Wagtail users through the Wagtail admin, and their state is associated with a [Wagtail Site](http://docs.wagtail.io/en/stable/reference/pages/model_reference.html#site).

### Basic usage

The Wagtail-Flags app provides two basic functions to check the status of feature flags, and one shortcut for checking the status of multiple flags.

- `flag_enabled` will return True if the feature flag is enabled. 

- `flag_disabled` will return True if the feature flag is disabled or does not exist.

- `flags_enabled` will return True only if all the given flags are enabled.


### In Python

In Python these functions can be imported from `flags.template_functions` and require a request object as the first argument (the request is used to check the flag's state for the requested Wagtail Site).

```python
from flags.template_functions import (
    flag_enabled,
    flag_disabled,
    flags_enabled
)

if flag_enabled(request, 'BETA_NOTICE'):
	print(“Beta notice banner will be displayed”)

if flag_disabled(request, 'BETA_NOTICE'):
	print(“Beta notice banner will not be displayed”)

if flags_enabled(request, 'FLAG1', 'FLAG2', 'FLAG3'):
	print(“All flags were set”)
```

In addition, a `flag_required` decorator is provided to require a particular flag for a Django view. The default behavior is to return a 404 if the flag is not set, but an optional fallback view function can be specified instead.

```python
from flags.decorators import flag_required

@flag_required('MY_FLAG')
def view_requiring_flag(request):
    retrun HttpResponse('flag was set')

def other_view(request):
    return HttpResponse('flag was not set')

@flag_required('MY_FLAG', fallback_view=other_view)
def view_with_fallback(request):
    return HttpResponse('flag was set')
```


### In Django templates

In Django templates you'll need to load the `feature_flags` template tag library. You can then use `flag_enabled`, `flag_disabled`, and `flags_enabled` tags:

```django
{% load feature_flags %}
{% flag_enabled 'BETA_NOTICE' as beta_flag %}
{% if beta_flag %}
  <div class="m-global-banner">
    I’m a beta banner.   
  </div>
{% endif %}
```


### In Jinja2 templates

The `flag_enabled`, `flag_disabled`, and `flags_enabled` functions can also be added to a Jinja2 environment and subsequently used in templates:

```python
from flags.template_functions import (
    flag_enabled,
    flag_disabled,
    flags_enabled
)

...

env.globals.update(
    flag_enabled=flag_enabled,
    flag_disabled=flag_disabled,
    flags_enabled=flags_enabled
)
```

```jinja
{% if flag_enabled(request, 'BETA_NOTICE') %}
  <div class="m-global-banner">
    I’m a beta banner.   
  </div>
{% endif %}
```


## Getting help

Please add issues to the [issue tracker](https://github.com/cfpb/wagtail-flags/issues).

## Getting involved

General instructions on _how_ to contribute can be found in [CONTRIBUTING](CONTRIBUTING.md).


----

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


----

## Credits and references

1. Forked from [cfgov-refresh](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/flags)
