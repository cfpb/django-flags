# Conditions

Conditions are functions that take a configured value and possible keyword arguments and determines whether the given arguments are equivalent to the value. Conditions are registered with a unique name that is exposed to users in Django settings and the Django admin.

```python
from flags import conditions
```

## Registering conditions

### `conditions.register(condition_name, fn=None, validator=None)`

Register a new condition, either as a decorator:

```python
from flags import conditions

@conditions.register('path', validator=conditions.validate_path)
def path_condition(path, request=None, **kwargs):
    return request.path.startswith(path)
```

Or as a function call:

```python
def path_condition(path, request=None, **kwargs):
    return request.path.startswith(path)

conditions.register('path', fn=path_condition, validator=conditions.validate_path)
```

Will raise a `conditions.DuplicateCondition` exception if the condition name is already registered.

A [validator](https://docs.djangoproject.com/en/stable/ref/validators/) can be given to validate the condition's expected value as provided by [the flag sources](../sources/).

## Exceptions

### `conditions.DuplicateCondition`

Exception raised by `conditions.register` if the condition name being registered is already registered.

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
