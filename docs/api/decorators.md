# Flag decorators

Decorators are provided for use with Django views and conditions that take a `request` argument. The default behavior is to return a 404 if a callable fallback is not given.

```python
from flags.decorators import (
    flag_check,
    flag_required,
)
```

## Checking state

### `flag_check(flag_name, state, fallback=None, **kwargs)`

Check that a given flag has the given state. If the state does not match, perform the fallback.

!!! note
    Because flags that do not exist are taken to be `False` by default, `@flag_check('MY_FLAG', False)` and `@flag_check('MY_FLAG', None)` will both succeed if `MY_FLAG` does not exist.

!!! note
    When a fallback view is given it *must* take the same arguments as the decorated view.

```python
from flags.decorators import flag_check

@flag_check('MY_FLAG', True)
def view_requiring_flag(request):
    return HttpResponse('MY_FLAG was true')

@flag_check('MY_OTHER_FLAG', False)
def view_requiring_other_flag_not_true(request):
    return HttpResponse('MY_OTHER_FLAG was False')

def fallback_view(request):
    return HttpResponse('MY_FLAG_WITH_FALLBACK was False')

@flag_check('MY_FLAG_WITH_FALLBACK', True, fallback=fallback_view)
def view_with_fallback(request):
    return HttpResponse('MY_FLAG_WITH_FALLBACK was True')
```


## Requiring state

### `flag_required(flag_name, fallback_view=None, pass_if_set=True)`

Require the given flag to be enabled.

!!! note
    When a fallback view is given it *must* take the same arguments as the decorated view.

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
