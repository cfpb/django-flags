# Conditions

Conditions are functions that take a configured value and possible keyword arguments and determines whether the given arguments are equivalent to the value. Conditions are registered with a unique name that is exposed to users in Django settings and the Django and Wagtail admin.

```python
from flags import conditions
```

## Registering conditions

### `conditions.register(condition_name, fn=None)`

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

## Exceptions

### `conditions.RequiredForCondition`

Exception intended to be raised when a condition is not given a keyword argument it requires for evaluation.

```python
@conditions.register('path')
def path_condition(path, request=None, **kwargs):
    if request is None:
        raise conditions.RequiredForCondition(
            "request is required for condition 'path'")

    return request.path.startswith(path)
```
