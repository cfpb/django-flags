# Conditions

## Built-in conditions

Django-Flags comes with the following conditions built-in:

### `boolean`

A simple boolean true/false intended to enable or disable a flag explicitly. The state of the flag evaluates to the value of the boolean condition.

```python
FLAGS = {'MY_FLAG': {'boolean': True}}
```

### `user`

Allows a flag to be enabled for the username given as the condition's value.

```python
FLAGS = {'MY_FLAG': {'user': 'jane.doe'}}
```

### `anonymous`

Allows a flag to be either enabled or disabled depending on the condition's boolean value.

```python
FLAGS = {'MY_FLAG': {'anonymous': False}}
```

### `parameter`

Allows a flag to be enabled based on a GET parameter with the name given as the condition's value.

```python
FLAGS = {'MY_FLAG': {'parameter': 'my_flag_param'}}
```

### `path`

Allows a flag to be enabled if the request's path matches the condition value.

```python
FLAGS = {'MY_FLAG': {'path': '/flagged/path'}}
```

### `after date`

Allows a flag to be enabled after a given date (and time) given in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601). The time must be specified either in UTC or as an offset from UTC.

```python
FLAGS = {'MY_FLAG': {'after date': '2017-06-01T12:00Z'}}
```

## Custom conditions

Custom conditions can be created and registered for use using the [conditions API](api/conditions).
