# Flagged URL patterns

Flagged URL patterns are an alternative to [flagging views with decorators](../../api/decorators).

```python
from flags.urls import flagged_path, flagged_paths, flagged_re_path, flagged_re_paths
```

### `flagged_path(flag_name, route, view, kwargs=None, name=None, state=True, fallback=None)`
### `flagged_re_path(flag_name, route, view, kwargs=None, name=None, state=True, fallback=None)`

Make a URL depend on the state of a feature flag. 

`flagged_path()` can be used in place of [Django's `path()`](https://docs.djangoproject.com/en/2.2/ref/urls/#django.urls.path).

`flagged_re_path()` can be used in place of [Django's `re_path()`](https://docs.djangoproject.com/en/2.2/ref/urls/#django.urls.re_path).

The `view` and the `fallback` can both be a set of `include()`ed patterns but any matching URL patterns in the includes must match *exactly* in terms of regular expression, keyword arguments, and name, otherwise a `404` may be unexpectedly raised. 

If a `fallback` is not given the flagged url will raise a `404` if the flag state does not match the required `state`. 

!!! note
    When a fallback view is given it *must* take the same arguments as the flagged view.

```python
urlpatterns = [
    flagged_path('MY_FLAG', 'a-url/', view_requiring_flag, state=True),
    flagged_re_path('MY_FLAG_WITH_FALLBACK', r'^another-url$', 
                    view_with_fallback, state=True, fallback=other_view)
    flagged_path('MY_FLAGGED_INCLUDE', 'myapp/', include('myapp.urls'),
                 state=True, fallback=other_view)
    flagged_re_path('MY_NEW_APP_FLAG', r'^mynewapp$', include('mynewapp.urls'),
                    state=True, fallback=include('myoldapp.urls'))
]
```

### `flagged_paths(flag_name, state=True, fallback=None)`
### `flagged_re_paths(flag_name, state=True, fallback=None)`

Flag multiple URLs in the same context with a context manager.

`flagged_paths()` returns a function that takes the same arguments as [Django's `path()`](https://docs.djangoproject.com/en/2.2/ref/urls/#django.urls.path) and which will flag the pattern's view.

`flagged_re_paths()` returns a function that takes the same arguments as [Django's `re_path()`](https://docs.djangoproject.com/en/2.2/ref/urls/#django.urls.re_path) and which will flag the pattern's view.

!!! note
    When a fallback view is given it *must* take the same arguments as the flagged view.

```python
with flagged_paths('MY_FLAG') as path:
    flagged_url_patterns = [
        path('a-url/', view_requiring_flag),
    ]

urlpatterns = urlpatterns + flagged_url_patterns
```
