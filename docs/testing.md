# Testing

## Testing code that depends on flags

Because `FLAGS` are definable in Django settings, you can use Django's standard `override_settings` to test with a flag off and on.

```python
from django.test import TestCase, override_settings

class FlaggedCodeTestCase(TestCase):
    @override_settings(FLAGS={"MY_FLAG": [("boolean", True)]})
    def test_flag_enabled(self):
        # Do the thing that requires the flag to be enabled

    @override_settings(FLAGS={"MY_FLAG": [("boolean", False)]})
    def test_flag_disabled(self):
        # Do the thing that requires the flag to be disabled
```

Alternatively, you can create a `FlagState` object along the same lines with a boolean condition that is `True` to test the flag-enabled code path, and then create one with a boolean condition that is` False` to test the not-enabled path.


```python
class FlaggedCodeTestCase(TestCase):
    def test_flag_enabled(self):
        FlagState.objects.create(
            name="MY_FLAG", condition="boolean", value="True"
        )
        # Do the thing that requires the flag to be enabled

    def test_flag_disabled(self):
        FlagState.objects.create(
            name="MY_FLAG", condition="boolean", value="True"
        )
        # Do the thing that requires the flag to be disabled
```
