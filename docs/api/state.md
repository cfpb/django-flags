# Flag state

```python
from flags.state import (
    flag_state,
    flag_enabled,
    flag_disabled,
    enable_flag,
    disable_flag,
)
```

!!! note
    If any of the flag state checking functions below is used at the top-level of a module (in `urls.py`, for example), it will be evaluated at import-time. This may have unintended consequences. [Database flag conditions](/api/sources/#flag-sources) may not be available, [custom conditions](/api/conditions/) may not be registered, and any dynamic change in flag state (such as date-based conditions or a newly added database condition) will not have an effect.

    Consider using [the flagged URLs API](/api/urls/) for state-checking in `urls.py`, [the view decorators](/api/decorators/) and [the class-based view mixin](/api/views/) for state-checking Django views, and using the state checking functions below inside methods and functions. This will have the added benefit of ensuring that the intention is clear, and that flagged code is as tightly-scoped as possible.

## Checking state

### `flag_state(flag_name, **kwargs)`

Return the value for the flag (`True` or `False`) by passing kwargs to its conditions. If the flag does not exist, this will return `None` so that existence can be introspected but will still evaluate to `False`.


## Requiring state

### `flag_enabled(flag_name, **kwargs)`

Returns `True` if a flag is enabled by passing kwargs to its conditions, otherwise returns `False`.

```python
if flag_enabled('MY_FLAG', request=a_request):
	print("My feature flag is enabled")
```

### `flag_disabled(flag_name, **kwargs)`

Returns `True` if a flag is disabled by passing kwargs to its conditions, otherwise returns `False`.

```python
if flag_disabled('MY_FLAG', request=a_request):
	print(“My feature flag is disabled”)
```


## Setting state

### `enable_flag(flag_name, create_boolean_condition=True, request=None)`

Enable a flag by adding or setting an existing database boolean condition to `True`. If the flag has other required conditions, those will take precedence. 

If `create_boolean_condition` is `False`, and a boolean database condition does not already exist, a `ValueError` will be raised.

### `disable_flag(flag_name, create_boolean_condition=True, request=None)`

Disable a flag by adding or setting an existing database boolean condition to `False`. If the flag has other required conditions, those will take precedence. 

If `create_boolean_condition` is `False`, and a boolean database condition does not already exist, a `ValueError` will be raised.

