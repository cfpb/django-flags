# Flag Sources

Django-Flags provides a means to provide custom flag sources using the [`FLAG_SOURCES` setting](../../settings/#flag_sources). Flag sources are classes that provide a `get_flags` method. The `get_flags` method must return a dictionary of flag name keys with a list of [`Condition`](#conditioncondition-value-requiredfalse) objects.

```python
from flags.sources import Condition


class CustomFlagSource(object):

    def get_flags(self):
        flags = {
            'MY_FLAG': [
                Condition('parameter', 'enable_my_flag'),
            ]
        }
        return flags
```

## API

### `get_flags(sources=None, ignore_errors=False)`

Return a dictionary of all flag names with [`Flag`](#flagname-conditions) objects that are available in the given `sources`. If `sources` is not given, the sources in the [`FLAG_SOURCES` setting](../../settings/#flag_sources) are used. If `ignore_errors` is `True`, any exceptions that occur when getting flags from a source will be caught and ignored.

### `Condition(condition, value, required=False)`

A simple wrapper around conditions.

#### `Condition.check(*kwargs)`

Check the condition against the given keyword arguments.

### `Flag(name, conditions=[])`

A simple wrapper around flags and their conditions. `conditions` is a list of [`Condition`](#conditioncondition-value-requiredfalse) objects.

#### `Flag.check_state(*kwargs)`

Check all of a flag's conditions and return the state based on the given keyword arguments.

