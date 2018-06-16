# Django-Flags

Feature flags allow you to toggle functionality in both Django settings and the Django admin based on configurable conditions.

## Dependencies

- Django 1.8+ (including Django 2.0)
- Python 2.7+, 3.6+

## Installation

First, install django-flags:

```shell
pip install django-flags
```

Then add `flags` as an installed app in your Django `settings.py`:

```python
INSTALLED_APPS = (
    ...
    'flags',
    ...
)
```

## Concepts

Feature flags in Django-Flags are identified by simple strings that are enabled when the conditions they are associated with are met. These flags can be used to wrap code and template content that should only be used when a flag is enabled or disabled.

Conditions determine whether a flag is enabled or disabled by comparing a defined expected value of some kind with the value at the time the flag is checked. In many cases, the flag is checked during a request, and some piece of the request's metadata is what is compared. For example, a feature flag that is enabled for a specific user would be enabled if the request's user matches the condition's user.

## Quickstart

To use Django-Flags you first need to define the flag, use the flag, and define conditions for the flag to be enabled.

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

Django 2.0:

```python
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(r'mypage/', TemplateView.as_view(template_name='mytemplate.html')),
]
```

Django 1.x:

```python
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^mypage/$', TemplateView.as_view(template_name='mytemplate.html')),
]
```

Then in the Django admin add conditions for the flag in "Settings", "Flags":

![Creating conditions in the Django admin](https://raw.githubusercontent.com/cfpb/django-flags/master/screenshot_create.png)

Then visiting the URL `/mypage?enable_my_flag=True` should show you the flagged `<div>` in the template.
