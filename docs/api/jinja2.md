# Jinja2 templates

Django-Flags provides an extension for adding the template tags to your Jinja2
backend configuration to enable the tags to be used in Jinja2 templates.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        ...
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        ...
        'OPTIONS': {
            'extensions': [
                ...
                'flags.jinja2tags.flags',  # add this line to your existing settings
                ...
            ],
        }
    },
]
```


## Checking state

### `flag_enabled`

Returns `True` if a flag is enabled, otherwise returns `False`.

```jinja
{% if flag_enabled('MY_FLAG') %}
  <div class="m-global-banner">
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

### `flag_disabled`

Returns `True` if a flag is disabled to its conditions, otherwise returns `False`.

```jinja
{% if flag_disabled('MY_FLAG') %}
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

```jinja
{% if flag_enabled('MY_FLAG_THAT_CHECKS_PAGE', page=page) %}
  This flag with a condition that uses the page object evaluated to True.
{% endif %}
```
