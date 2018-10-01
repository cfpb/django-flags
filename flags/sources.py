
from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string

from flags.conditions import get_condition


class SettingsFlagsSource(object):

    def get_flags(self):
        settings_flags = getattr(settings, 'FLAGS', {}).items()
        flags = {}
        for flag, conditions in settings_flags:
            # Flag conditions in settings used to be dicts. We expect 2-tuples
            # now but contiune to support dicts. At some point, we should issue
            # deprecation warnings about dicts and then deprecate support.
            if isinstance(conditions, dict):
                conditions = conditions.items()
            flags[flag] = [Condition(c, v, source=self) for c, v in conditions]

        return flags


class DatabaseFlagsSource(object):

    def get_queryset(self):
        FlagState = apps.get_model('flags', 'FlagState')
        return FlagState.objects.all()

    def get_flags(self):
        flags = {}
        for o in self.get_queryset():
            if o.name not in flags:
                flags[o.name] = []
            flags[o.name].append(Condition(
                o.condition, o.value, source=self, obj=o
            ))

        return flags


class Condition:
    """ A simple wrapper around conditions """

    def __init__(self, condition, value, source=None, obj=None):
        self.condition = condition
        self.value = value
        self.checkers = get_condition(self.condition)
        self.source = source
        self.obj = obj

    def __eq__(self, other):
        return other.condition == self.condition and other.value == self.value

    def check(self, **kwargs):
        return any(c(self.value, **kwargs) for c in self.checkers)


class Flag:
    """ A simple wrapper around feature flags and their conditions """

    def __init__(self, name, conditions=[]):
        self.name = name
        self.conditions = conditions

    def __eq__(self, other):
        """ There can be only one feature flag of a given name """
        return other.name == self.name

    def check_state(self, **kwargs):
        """ Determine this flag's state based on any of its conditions """
        return any(c.check(**kwargs) for c in self.conditions)


def get_flags(sources=None):
    """ Get all flag sources sources defined in settings.FLAG_SOURCES.
    FLAG_SOURCES is expected to be a list of Python paths to classes providing
    a get_flags() method that returns a dict with the same format as the
    FLAG setting. """
    flags = {}

    if sources is None:
        sources = getattr(settings, 'FLAG_SOURCES', (
            'flags.sources.SettingsFlagsSource',
            'flags.sources.DatabaseFlagsSource',
        ))

    for source_str in sources:
        source_cls = import_string(source_str)
        source_obj = source_cls()
        source_flags = source_obj.get_flags()

        for flag, conditions in source_flags.items():
            if flag in flags:
                flags[flag].conditions += conditions
            else:
                flags[flag] = Flag(flag, conditions)

    return flags
