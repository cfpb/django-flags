# Release Notes

## Pending

### What's new?

- Updated packaging to pyproject.toml and linting/formatting to ruff
- Added Django 5.0 support (thanks [@adamchainz](https://github.com/adamchainz)!)

## 5.0.13

### What's new?

- Modernize code for Python 3.6+ (thanks [@adamchainz](https://github.com/adamchainz)!)
- Run linters with Python 3.11 (thanks [@adamchainz](https://github.com/adamchainz)!)
- Format with Black 23 (thanks [@adamchainz](https://github.com/adamchainz)!)
- Added Django 4.2 support (thanks [@adamchainz](https://github.com/adamchainz)!).

### Removals

- Removed Python 3.6 support (thanks [@michael-k](https://github.com/michael-k)!).

### Bug fixes

- Removed errant print statement (thanks [@Natim](https://github.com/Natim)!).


## 5.0.12

### What's new?

- Added Django 4.1 support (thanks [@adamchainz](https://github.com/adamchainz)!).


## 5.0.11

### What's new?

- Added changelog and documentation links to the package on PyPI (thanks [@adamchainz](https://github.com/adamchainz)!)


## 5.0.10

### What's new?

- Fixed an issue with resolving `include()`s in `flagged_path()` URL patterns ([#100](https://github.com/cfpb/django-flags/issues/100))


## 5.0.9

### What's new?

- Fixed a `DeprecationWarning` on Jinja 3+.
- Fixed an `AttributeError` on `AnonymousUser` in the user condition (thanks [@edomora97](https://github.com/edomora97)!)


## 5.0.8

### What's new?

- Prevent `RemovedInDjango41Warning` about `default_app_config` for Django 3.2+ (thanks [@adamchainz](https://github.com/adamchainz)!)

## 5.0.7

### What's new?

- Update Django 4 pin to allow versions under 4.1


## 5.0.6

### What's new?

- Added Django 4.0 support (thanks [@gregtap](https://github.com/gregtap)!)


## 5.0.5

### What's new?

- Added Django 3.2 support (thanks [@dduong42](https://github.com/dduong42)!)


## 5.0.4

### What's new?

- Fixed the "path matches" condition validator to allow any valid regular expression.


## 5.0.3

### What's new?

- Added [`enable_flag`](../api/state/#enable_flagflag_name-create_boolean_conditiontrue-requestnone) and [`disable_flag`](../api/state/#disable_flagflag_name-create_boolean_conditiontrue-requestnone) functions.
- Added [`enable_flag`](../management_commands/#enable_flag-flag_name) and [`disable_flag`](../management_commands/#disable_flag-flag_name) management commands.


## 5.0.2

### What's new?

- Added defaults for `FlaggedViewMixin`'s `kwargs` (by [@jackton1](https://github.com/jackton1))


## 5.0.1

### What's new?

- Added Django 3.1 support


## 5.0.0

### What's new?

- Added Django 3.0 support
- Added validator support to ensure that the values that flag conditions test against are valid.

### Deprecations

- Deprecated the optional `flags.middleware.FlagConditionsMiddleware` in favor of always lazily caching flags on the request object.

### Removals

- Django Flags 4.1 deprecated support for using a single dictionary to hold key/values of conditions for a settings-based feature flag, and this has been removed. Use [a list of dictionaries or tuples instead](/settings/#flags).
- Removed support for Django 1.11.


## 4.2.4

### What's new?

- `FLAGS_STATE_LOGGING` is now `False` by default to cut down on potentially unwanted noise ([@darakian](https://github.com/darakian)).


## 4.2.3

### What's new?

- Removed the word "optional" to describe non-required conditions in the [Flag Conditions Debug Toolbar panel](https://cfpb.github.io/django-flags/debugging/#django-debug-toolbar-panels).


## 4.2.2

### What's new?

- Fixed a bug where if a flag was defined in multiple [sources](/settings#flag_sources) the conditions defined in subsequent sources would not be evaluated. This means (with the default sources) if a flag is defined in Django settings and has conditions defined the database, only the settings conditions would be evaluated.


## 4.2.1

### What's new?

- Made the language around optional boolean conditions with required conditions clearer in the [Flag Conditions Debug Toolbar panel](https://cfpb.github.io/django-flags/debugging/#django-debug-toolbar-panels)


## 4.2.0

### What's new?

- Added optional [Django Debug Toolbar panels](https://cfpb.github.io/django-flags/debugging/#django-debug-toolbar-panels) to [list all flag conditions](https://cfpb.github.io/django-flags/debugging/#flag-conditions) and to [report flag checks for a request](https://cfpb.github.io/django-flags/debugging/#flag-checks).
- Added flag state check logging and [`FLAGS_STATE_LOGGING` setting](https://cfpb.github.io/django-flags/settings/#flags_state_logging) to enable it.
- Modified flag state checking to raise an `AppRegistryNotReady` if an attempt to check flag state is made before the app registry is ready.
- Modified flag view decorators to warn if a fallback view do not take the same arguments as the flag view.

## 4.1.2

### What's new?

- Added support for [Django 2.2](https://docs.djangoproject.com/en/2.2/releases/2.2/) and [Python 3.7](https://docs.python.org/3/whatsnew/3.7.html) (Chris Adams).

## 4.1.1

### What's new?

- `boolean` and `anonymous` conditions now accept [multiple possible string representations of truth](/conditions/#boolean) as their values.
- `parameter` conditions now accept [possible parameter values](http://localhost:7777/conditions/#parameter).

## 4.1

### What's new?

- Added the option to specifiy [required conditions](/usage/#defining-flags) that must always be met.
- Deprecated support for using a single dictionary to hold key/values of conditions for a settings-based feature flag. Support will be removed in Django-Flags 5.0. Use [a list of dictionaries or tuples instead](/settings/#flags).
- Added a [`before date` condition](/conditions) that is met whenever the current date is before the expected date.

## 4.0.3

### What's new?
- The system check introduced in 4.0.2 will no longer raise a `ProgrammingError` or an `OperationalError` when run pre-migration.

## 4.0.2

### What's new?
- Logging of non-existent conditions is now a Django system check.

## 4.0.1

### What's new?
- `condition.check()` returns a Falsy `None` instead of raising a `TypeError` when a configured condition has no function registered.

## 4.0

### What's new?

- The template functions `flag_enabled` and `flag_disabled` in both [Django](/api/django) and [Jinja2](/api/jinja2) templates now support taking keyword arguments that could be used by [custom conditions](/api/conditions).
- Jinja2 template functions are now available via a Jinja2 extension that can be [included in `settings.py`](/api/jinja2).
- The optional `flags.middleware.FlagConditionsMiddleware` has been added to ensure that all feature flag checks throughout single request cycle use the same flag conditions.
- Support for specifying the [source of feature flags in `settings.py`](/settings#flag_sources) has been added to allow further customization and the potential to limit flags to settings or database-only.
- The "user" condition now supports custom user models. ([@callorico](https://github.com/callorico))

### Upgrading

Django-Flags 4.0 introduces backwards-incompatible changes for users of Jinja2 templates.

Previously Django-Flags provided `flags.template_functions.flag_enabled` and `flags.template_functions.flag_disabled` functions that had to be registered in the Jinja2 environment downstream. The Django-Flags documentation recommended doing so in `jinja2.Environment.globals.update()`. **`flags.template_functions` has been removed in Django-Flags 4.0.**

Jinja2 function registration is now handled by a `flags.jinja2tags.flags` Jinja2 extension. To use Django-Flags 4.0 with Jinja2 templates, the `TEMPLATES` setting in `settings.py` should to be modified to include the extension:

```python
TEMPLATES = [
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

## 3.0.2

### What's new?

- Requests are now optional the `flag_enabled` and `flag_disabled` template tags.
- Flag state form conditions are now bound when the form is created to ensure all custom conditions are available on the form. ([@callorico](https://github.com/callorico))

## 3.0.1

### What's new?

- Django 2.1 is now supported.

## 3.0

Django-Flags is a fork of the Django-only components of the [Wagtail-Flags](https://github.com/cfpb/wagtail-flags) feature flag library. This is the initial release.

