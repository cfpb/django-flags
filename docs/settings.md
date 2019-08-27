# Settings

## Defining flags

### `FLAG_SOURCES`

Default: `('flags.sources.SettingsFlagsSource', 'flags.sources.DatabaseFlagsSource',)`

A list or tuple containing the full Python path strings to classes that provides a [`get_flags()` method](../api/sources/#flag-sources). The `get_flags()` method is expected to return a dictionary of flags and [`Condition` objects](../api/sources/#conditioncondition-value-requiredfalse). All flags returned by all flag sources will be available to check.

### `FLAGS`

Default: `{}`

A dictionary of feature flags and optional conditions used when `'flags.sources.SettingsFlagsSource'` is in [`FLAG_SOURCES`](#flag_sources).

Conditions can either be included as:

- A list of dictionaries with the format:
  ```python
  {'condition': 'condition name', 'value': 'expected value', 'required': True}`
  ```
  or
  ```python
  {'condition': 'condition name', 'value': 'expected value'}
  ``` 
  (`required` defaults to `False`).
- A list of 3-tuples with the format: 
  ```python
  (condition name, expected value, required)
  ```
- A list of 2-tuples with the format:
  ```python
  (condition name, expected value)
  ```
  (`required` defaults to `False`)

For example:

```python
FLAGS = {
  'FLAG_WITH_EMPTY_CONDITIONS': [],
  'FLAG_WITH_DICT_CONDITIONS': [
    {'condition': 'condition name', 'value': 'expected value to be enabled'},
    {'condition': 'condition name', 'value': 'expected value to be enabled', 'required': True},
  ],
  'FLAG_WITH_TUPLE_CONDITIONS': [
    ('condition name', 'expected value to be enabled'),
    ('condition name', 'expected value to be enabled', True),
  ],
  # This is possible, but not recommended
  'FLAG_WITH_MIXED_CONDITIONS': [
    {'condition': 'condition name', 'value': 'expected value to be enabled'},
    ('condition name', 'expected value to be enabled', True),
  ],
}
```

Previously flag definitions in `FLAGS` supported a single dictionary (rather than a list) with the condition name as the key and expected value as value. This method of specifying flags is deprecated and will be removed in Django-Flags 5.0.

### `FLAGS_STATE_LOGGING`

Default: `False`

If this setting is `True` Django-Flags will log all flag state checks with how the conditions were evaluated. These will appear in the log file like:

```
INFO:flags.sources:Flag MY_FLAG evaluated False with conditions: boolean (False).
INFO:flags.sources:Flag MY_FLAG evaluated True with conditions: boolean (False), path matches (True).
```

This is intended for use in tracking the history and usage of enabled featured flags.
