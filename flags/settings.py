
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

from flags.conditions import get_condition


class Flag:
    """ A simple wrapper around feature flags and their conditions """

    def __init__(self, name, conditions_spec={}):
        self.name = name
        self.__conditions_spec = conditions_spec

    def __eq__(self, other):
        """ There can be only one feature flag of a given name """
        return other.name == self.name

    @cached_property
    def conditions(self):
        """ Get all flag conditions configured in settings """
        # Get condition callables for our settings-configured conditions
        conditions = [
            (c, fn, v, None)
            for c, v in self.__conditions_spec.items()
            for fn in get_condition(c)
        ]
        return conditions

    def check_state(self, **kwargs):
        """ Determine this flag's state based on any of its conditions """
        return any(fn(v, **kwargs) for c, fn, v, o in self.conditions)


def get_flags_from_sources(sources=None):
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
        source_flags = source_cls().get_flags()

        for flag, conditions in source_flags.items():
            if flag in flags:
                flags[flag].update(conditions)
            else:
                flags[flag] = conditions

    return flags


def get_flags(sourced_flags=None):
    """ Get a dictionary of Flag objects for all flags.
    This combines FLAGS from settings with all possible FLAG_SOURCES. """
    if sourced_flags is None:
        sourced_flags = get_flags_from_sources()

    flags = {
        name: Flag(name, conditions_spec=conditions)
        for name, conditions in sourced_flags.items()
    }
    return flags
