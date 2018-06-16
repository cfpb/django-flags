# Django templates

Wagtail-Flags provides a template tag library that can be used to evaluate flags in Django templates.

```django
{% load feature_flags %}
```

## Checking state

### `flag_enabled`

Returns `True` if a flag is enabled by passing the current request to its conditions, otherwise returns `False`.

```django
{% flag_enabled 'MY_FLAG' as my_flag %}
{% if my_flag %}
  <div class="m-global-banner">
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

### `flag_disabled`

Returns `True` if a flag is disabled by passing the current request to its conditions, otherwise returns `False`.

```django
{% flag_disabled 'MY_FLAG' as my_flag %}
{% if my_flag %}
  <div class="m-global-banner">
    I’m the result of a feature flag that is not enabled.
  </div>
{% endif %}
```
