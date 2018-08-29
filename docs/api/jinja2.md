# Jinja2 templates

Django-Flags provides template functions that can be added to a Jinja2 environment and subsequently used in templates.

```python
from flags.template_functions import (
    flag_enabled,
    flag_disabled
)
from jinja2 import Environment

...

env = Environment(…)
env.globals.update(
    flag_enabled=flag_enabled,
    flag_disabled=flag_disabled
)
```

## Checking state

### `flag_enabled`

Returns `True` if a flag is enabled by for the given request, otherwise returns `False`.

```jinja
{% if flag_enabled('MY_FLAG', request) %}
  <div class="m-global-banner">
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

`request` is optional.

### `flag_disabled`

Returns `True` if a flag is disabled by passing the current request to its conditions, otherwise returns `False`.
Returns `True` if a flag is disabled by for the given request, otherwise returns `False`.

```jinja
{% if flag_disabled('MY_FLAG', request) %}
  <div class="m-global-banner">
    I’m the result of a feature flag that is not enabled.
  </div>
{% endif %}
```

`request` is optional.
