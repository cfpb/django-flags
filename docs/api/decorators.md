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

**Note**, because flags that do not exist are taken to be `False` by default, `@flag_check('MY_FLAG', False)` and `@flag_check('MY_FLAG', None)` will both succeed if `MY_FLAG` does not exist.

```python
from flags.decorators import flag_check

@flag_check('MY_FLAG', True)
def view_requiring_flag(request):
    return HttpResponse('flag was set')

@flag_check('MY_OTHER_FLAG', False)
def view_when_other_flag_is_set(request):
    return HttpResponse('flag was set')

def other_view(request):
    return HttpResponse('always available')

@flag_check('MY_FLAG_WITH_FALLBACK', True, fallback=other_view)
def view_with_fallback(request):
    return HttpResponse('flag was set')
```

## Requiring state

### `flag_required(flag_name, fallback_view=None, pass_if_set=True)`

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
