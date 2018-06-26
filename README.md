# Django-Flags

[![Build Status](https://travis-ci.org/cfpb/django-flags.svg?branch=master)](https://travis-ci.org/cfpb/django-flags)
[![Coverage Status](https://coveralls.io/repos/github/cfpb/django-flags/badge.svg?branch=master)](https://coveralls.io/github/cfpb/django-flags?branch=master)

Feature flags allow you to toggle functionality in both Django code and the Django templates based on configurable conditions. Flags can be useful for staging feature deployments, for A/B testing, or for any time you need an on/off switch for blocks of code. The toggle can be by date, user, URL value, or a number of [other conditions](https://cfpb.github.io/django-flags/conditions/), editable in the admin or in definable in settings.

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Documentation](#documentation)
- [Getting help](#getting-help)
- [Getting involved](#getting-involved)
- [Licensing](#licensing)
- [Credits and references](#credits-and-references)

## Dependencies

- Django 1.8+ (including Django 2.0)
- Python 2.7+, 3.6+

## Installation

1. Install Django-Flags:

```shell
pip install django-flags
```

2. Add `flags` as an installed app in your Django `settings.py`:

 ```python
 INSTALLED_APPS = (
     ...
     'flags',
     ...
 )
```

## Documentation

https://cfpb.github.io/django-flags is the full documentation for Django-Flags, and includes how to get started, general usage, and an API reference. 

## Getting help

Please add issues to the [issue tracker](https://github.com/cfpb/django-flags/issues).

## Getting involved

General instructions on _how_ to contribute can be found in [CONTRIBUTING](CONTRIBUTING.md).

## Licensing
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

## Credits and references

Django-Flags was forked from [Wagtail-Flags](https://github.com/cfpb/wagtail-flags), which was itself forked from [cfgov-refresh](https://github.com/cfpb/cfgov-refresh).
