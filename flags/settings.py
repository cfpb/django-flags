from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.utils.functional import cached_property

from flags.conditions import get_condition


# Private set of all flags from sources in FLAG_SOURCES. This is
# populated on AppConfig.ready() by add_flags_from_sources below.
SOURCED_FLAGS = {}


class DuplicateFlagException(Exception):
    """ Raised when flags are defined in multiple places """


class Flag:
    """ A simple wrapper around feature flags and their conditions """

    def __init__(self, name, configured_conditions={}):
        self.name = name
        self.__configured_conditions = configured_conditions

    def __eq__(self, other):
        """ There can be only one feature flag of a given name """
        return other.name == self.name

    @cached_property
    def configured_conditions(self):
        """ Get all flag conditions configured in settings """
        # Get condition callables for our settings-configured conditions
        conditions = [
            (c, v, None)
            for c, v in self.__configured_conditions.items()
        ]
        return conditions

    @property
    def dynamic_conditions(self):
        """ Get dynamic flag conditions from models.FlagState """
        # Get condition callables for our dynamic-configured conditions
        FlagState = apps.get_model('flags', 'FlagState')
        conditions = [
            (s.condition, s.value, s)
            for s in FlagState.objects.filter(name=self.name)
        ]
        return conditions

    @property
    def conditions(self):
        """ Get all flag conditions """
        return self.configured_conditions + self.dynamic_conditions

    def check_state(self, **kwargs):
        """ Determine this flag's state based on any of its conditions """
        return any(
            fn(v, **kwargs)
            for c, v, o in self.conditions
            for fn in get_condition(c)
        )


def add_flags_from_sources(sources=None):
    """ Read flags from sources defined in settings.FLAG_SOURCES.
    FLAG_SOURCES is expected to be a list of Python module with flags
    specified with variable assignment, e.g. MY_FLAG = True """
    global SOURCED_FLAGS
    flags = getattr(settings, 'FLAGS', {})

    if sources is None:
        sources = getattr(settings, 'FLAG_SOURCES', ())

    for source_str in sources:
        source = import_module(source_str)
        for flag in (f for f in dir(source)
                     if f.isupper() and isinstance(getattr(source, f), bool)):
            if flag in flags or flag in SOURCED_FLAGS:
                raise DuplicateFlagException("{} duplicated in {}".format(
                    flag, source_str))

            cache.delete('flags_conditions_' + flag)
            SOURCED_FLAGS[flag] = getattr(source, flag)


def get_flags(sourced_flags=None):
    """ Get a dictionary of Flag objects for all flags.
    This combines FLAGS from settings with all possible FLAG_SOURCES. """
    FLAGS_CACHE_CONDITIONS = getattr(settings, 'FLAGS_CACHE_CONDITIONS', False)
    FLAGS_CACHE_KEY = getattr(settings, 'FLAGS_CACHE_KEY', 'flags')
    flags = None

    if FLAGS_CACHE_CONDITIONS:
        flags = cache.get(FLAGS_CACHE_KEY)

    if flags is None:
        flags_spec = getattr(settings, 'FLAGS', {})
        if sourced_flags is None:
            sourced_flags = SOURCED_FLAGS

        flags_spec.update(sourced_flags)
        flags = {
            name: Flag(name, configured_conditions=conditions)
            for name, conditions in flags_spec.items()
        }

        if FLAGS_CACHE_CONDITIONS:
            cache.set(FLAGS_CACHE_KEY, flags)

    return flags
