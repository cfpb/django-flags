# Settings

## Defining flags

### `FLAGS`

Default: `{}`

A dictionary of available feature flags and optional conditions. Flags must be defined in this dictionary to be available in the Django Admin for users to add and remove conditions that way.

This dictionary takes the following format:

```python
FLAGS = {
  'FLAG_WITH_EMPTY_CONDITIONS': {}
  'FLAG_WITH_CONDITIONS': {
    'condition name': 'value flag is expected to match to be enabled',
  }
}
```
