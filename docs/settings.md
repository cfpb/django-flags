# Settings

## Defining flags

### `FLAG_SOURCES`

Default: `('flags.sources.SettingsFlagsSource', 'flags.sources.DatabaseFlagsSource',)`

A list or tuple containing the full Python path strings to classes that provides a [`get_flags()` method](../api/sources/#flag-sources). All flags returned by all flag sources will be available to check.

### `FLAGS`

Default: `{}`

A dictionary of feature flags with a list of optional conditions and metadata used when `'flags.sources.SettingsFlagsSource'` is in [`FLAG_SOURCES`](#flag_sources).

Each key is the name of a feature flag, and the value should be a list contining conditions and metadata for that flag.

Individual conditions are defined in a dictionary with the format:

```python
{'condition': 'condition name', 'value': 'expected value'}
{'condition': 'condition name', 'value': 'expected value', 'required': True}
``` 

(`required` defaults to `False`).

Metadata is defined in a dictionary along with conditions with in the format:

```python
{'help_text': 'enable a cool new future', 'category': 'temporary'}
```

There should be only one metadata dictionary per flag. Any dictionary within the feature flag's list that does not contain `condition` and `value` keys will be treated as the metadata dictionary.

For example:

```python
FLAGS = {
  'FLAG_WITH_EMPTY_CONDITIONS': [],
  'FLAG_WITH_CONDITIONS': [
    {'condition': 'condition name', 'value': 'expected value to be enabled'},
    {'condition': 'condition name', 'value': 'expected value to be enabled', 'required': True},
  ],
  'FLAG_WITH_METADATA': [
    {'condition': 'condition name', 'value': 'expected value to be enabled'},
    {'help_text': 'a human-friendly flag description', 'category': 'a human-friendly category'},
  ],
}
```

For brevity, conditions can also be defined as either 2- or 3- tuples:

```python
(condition name, expected value),
(condition name, expected value, required),
("_metadata": {"key": "value"}),
```

### `FLAGS_STATE_LOGGING`

Default: `False`

If this setting is `True` Django-Flags will log all flag state checks with how the conditions were evaluated. These will appear in the log file like:

```
INFO:flags.sources:Flag MY_FLAG evaluated False with conditions: boolean (False).
INFO:flags.sources:Flag MY_FLAG evaluated True with conditions: boolean (False), path matches (True).
```

This is intended for use in tracking the history and usage of enabled featured flags.
