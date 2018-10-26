
from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string

from flags.conditions import get_condition


class Condition(object):
    """ A simple wrapper around conditions """

    def __init__(self, condition, value):
        self.condition = condition
        self.value = value
        self.fn = get_condition(self.condition)

    def __eq__(self, other):
        return other.condition == self.condition and other.value == self.value

    def check(self, **kwargs):
        return self.fn(self.value, **kwargs)


class Flag(object):
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
            flags[flag] = [Condition(c, v) for c, v in conditions]

        return flags


class DatabaseCondition(Condition):
    """ Condition that includes the FlagState database object """

    def __init__(self, condition, value, obj=None):
        super(DatabaseCondition, self).__init__(condition, value)
        self.obj = obj


class DatabaseFlagsSource(object):

    def get_queryset(self):
        FlagState = apps.get_model('flags', 'FlagState')
        return FlagState.objects.all()

    def get_flags(self):
        flags = {}
        for o in self.get_queryset():
            if o.name not in flags:
                flags[o.name] = []
            flags[o.name].append(DatabaseCondition(
                o.condition, o.value, obj=o
            ))

        return flags


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
