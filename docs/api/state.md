# Flag state

```python
from flags.state import (
    flag_state,
    flag_enabled,
    flag_disabled,
)
```

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
