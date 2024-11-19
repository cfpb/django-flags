# Conditions

## Built-in conditions

Django-Flags comes with the following conditions built-in:

### `boolean`

A simple boolean true/false intended to enable or disable a flag explicitly. The state of the flag evaluates to the value of the boolean condition.


```python
FLAGS = {'MY_FLAG': [{'condition': 'boolean', 'value': True}]}
```

The value can given as a Python `True` or `False` or  as any [string representation of truth](https://docs.python.org/3/distutils/apiref.html#distutils.util.strtobool), such as `y`, `yes`, `t`, `true`, `on` and `1` for true values, and `n`, `no`, `f`, `false`, `off` and `0` for false values.

### `user`

Allows a flag to be enabled for the username given as the condition's value.

```python
FLAGS = {'MY_FLAG': [{'condition': 'user', 'value': 'jane.doe'}]}
```

### `anonymous`

Allows a flag to be either enabled or disabled depending on whether a user is anonymous (not logged in) to Django.

```python
# MY_FLAG is enabled if the user is not anonymous (is logged in)
FLAGS = {'MY_FLAG': [{'condition': 'anonymous', 'value': False}]}
```

The value can given as a Python `True` or `False` or  as any [string representation of truth](https://docs.python.org/3/distutils/apiref.html#distutils.util.strtobool), such as `y`, `yes`, `t`, `true`, `on` and `1` for true values, and `n`, `no`, `f`, `false`, `off` and `0` for false values.

### `parameter`

Allows a flag to be enabled by including a parameter in the request's query string. `value` is the name of the parameter, or a name and expected value. If an expected value isn't provided, the value must be `True`.

```python
FLAGS = {
    'MY_FLAG': [
        {'condition': 'parameter', 'value': 'my_flag_param1'},      # ?my_flag_param1=True
        {'condition': 'parameter', 'value': 'my_flag_param2=now'},  # ?my_flag_param2=now
        {'condition': 'parameter', 'value': 'my_flag_param3='},     # ?my_flag_param3
    ]
}
```

### `path matches`

Allows a flag to be enabled if the request's path matches the regular expression value.

```python
FLAGS = {'MY_FLAG': [{'condition': 'path matches', 'value': r'^/flagged/path'}]}
```

### `after date`

Allows a flag to be enabled after a given date (and time) given in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601). The time must be specified either in UTC or as an offset from UTC.

```python
FLAGS = {'MY_FLAG': [{'condition': 'after date', 'value': '2017-06-01T12:00Z'}]}
```

### `before_date`

Allows a flag to be enabled before a given date (and time) given in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601). The time must be specified either in UTC or as an offset from UTC.

```python
FLAGS = {'MY_FLAG': {'before date': '2022-06-01T12:00Z'}}
```

## Custom conditions

Custom conditions can be created and registered for use using the [conditions API](../api/conditions).
