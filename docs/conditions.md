# Conditions

## Built-in conditions

Django-Flags comes with the following conditions built-in:

### `boolean`

A simple boolean true/false intended to enable or disable a flag explicitly. The state of the flag evaluates to the value of the boolean condition.

```python
FLAGS = {'MY_FLAG': [{'condition': 'boolean', 'value': True}]}
```

The value can be given as a Python `True` or `False` Boolean value or as the strings `"true"`, `"True"`, `"False"`, or `"false"`.

### `user`

Allows a flag to be enabled for the username given as the condition's value.

```python
FLAGS = {'MY_FLAG': [{'condition': 'user', 'value': 'jane.doe'}]}
```

### `anonymous`

Allows a flag to be either enabled or disabled depending on the condition's boolean value.

```python
FLAGS = {'MY_FLAG': [{'condition': 'anonymous', 'value': False}]}
```

The value can be given as a Python `True` or `False` Boolean value or as the strings `"true"`, `"True"`, `"False"`, or `"false"`.

### `parameter`

Allows a flag to be enabled if a GET parameter with the condition's value as its name exists for a request.

```python
FLAGS = {'MY_FLAG': [{'condition': 'parameter', 'value': 'my_flag_param'}]}
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

Custom conditions can be created and registered for use using the [conditions API](api/conditions).
