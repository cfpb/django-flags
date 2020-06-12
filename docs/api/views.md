# Class-based views

```python
from flags.views import (
    FlaggedViewMixin,
    FlaggedTemplateView,
)
```

## API

### `FlaggedViewMixin`

Adds flag-checking to HTTP method dispatching in [class-based views](https://docs.djangoproject.com/en/2.2/topics/class-based-views/).

#### Attributes

<dl>
  <dt>`flag_name`</dt>
  <dd>The feature flag this view depends on.</dd>

  <dt>`state`</dt>
  <dd>Either `True` or `False`, the state the feature flag should be in. By default, `state` is `True`, requiring the flag to evaluate to `True`.</dd>

  <dt>`fallback`</dt>
  <dd>A view to fallback on if the flag does not match the required `state`. Defaults to `None`, causing the view to raise a `404` if the flag does not match the required `state`.</dd>
</dl> 

!!! note
    When a fallback view is given it *must* take the same arguments as the flagged view.

For example, in `views.py`:

```python
from django.views.generic import View
from flags.views import FlaggedViewMixin

class MyFlaggedView(FlaggedViewMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('ok')
```

And in `urls.py`:

```python
from django.urls import path
from flags.urls import flagged_path

urlpatterns = [
    path('my-url/', MyFlaggedView.as_view(flag_name='MY_FLAG'))
]
```

### `FlaggedTemplateView`

A combination of [`TemplateView`](https://docs.djangoproject.com/en/2.2/ref/class-based-views/base/#templateview) and [`FlaggedViewMixin`](#flaggedviewmixin).

For example, in `views.py`:

```python
from flags.views import FlaggedTemplateView

class MyFlaggedView(FlaggedTemplateView):
    template_name = "mytemplate.html"
    flag_name = 'MY_FLAG'
```

Or to serve a template directly in `urls.py`:

```
from django.urls import path
from flags.views import FlaggedTemplateView

urlpatterns = [
    path(
        'my_url/', 
        FlaggedTemplateView.as_view(
            template_name='mytemplate.html', 
            flag_name='MY_FLAG'
        )
    ),
]
```
