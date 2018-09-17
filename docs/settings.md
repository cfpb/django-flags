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

## Caching flag conditions

### `FLAGS_CACHE_CONDITIONS`

Default: `False`

When set to `True`, Django-Flags will store conditions in the default [Django Cache](https://docs.djangoproject.com/en/2.1/topics/cache/#setting-up-the-cache). Saving or deleting a condition in the Django admin will invalidate the cache. 

### `FLAGS_CACHE_KEY` 

Default: `'flags'`

When `FLAGS_CACHE_CONDITIONS` is `True`, the `FLAGS_CACHE_KEY` string will be the key used to cache flag conditions. 
