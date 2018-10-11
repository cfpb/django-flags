# Django templates

Django-Flags provides a template tag library that can be used to evaluate flags in Django templates.

```django
{% load feature_flags %}
```

## Checking state

### `flag_enabled`

Returns `True` if a flag is enabled, otherwise returns `False`.

```django
{% flag_enabled 'MY_FLAG' as my_flag %}
{% if my_flag %}
  <div class="m-global-banner">
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

### `flag_disabled`

Returns `True` if a flag is disabled, otherwise returns `False`.

```django
{% flag_disabled 'MY_FLAG' as my_flag %}
{% if my_flag %}
  <div class="m-global-banner">
    I’m the result of a feature flag that is not enabled.
  </div>
{% endif %}
```

If a `request` exists in the current context,
it will be passed to any conditions that use it.


## Passing additional arguments

Some conditions take additional keyword arguments.
For example, you could pass a `page` object:

```django
{% flag_enabled 'MY_FLAG_THAT_CHECKS_PAGE' page=page as my_flag %}
{% if my_flag %}
  This flag with a condition that uses the page object evaluated to True.
{% endif %}
```
