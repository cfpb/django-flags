import logging
import warnings

from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string

from flags.conditions import RequiredForCondition, get_condition


logger = logging.getLogger(__name__)


class Condition(object):
    """ A simple wrapper around conditions """

    def __init__(self, condition, value, required=False):
        self.condition = condition
        self.value = value
        self.fn = get_condition(self.condition)
        self.required = required

    def __eq__(self, other):
        return other.condition == self.condition and other.value == self.value

    def check(self, **kwargs):
        if self.fn is not None:
            try:
                return self.fn(self.value, **kwargs)
            except RequiredForCondition:
                logger.exception(
                    'Missing required argument for condition {}'.format(
                        self.condition
                    )
                )


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
        not_required = [c for c in self.conditions if not c.required]
        required = [c for c in self.conditions if c.required]

        if len(not_required) == 0 and len(required) == 0:
            return False

        return (
            any(c.check(**kwargs) for c in not_required)
            if len(not_required) > 0
            else True
        ) and (
            all(c.check(**kwargs) for c in required)
        )


class SettingsFlagsSource(object):

    def get_flags(self):
        settings_flags = getattr(settings, 'FLAGS', {}).items()
        flags = {}
        for flag, conditions in settings_flags:
            # Flag conditions in settings used to be dicts, which are now
            # deprecated.
            if isinstance(conditions, dict):
                warnings.warn(
                    'dict feature flag definitions are deprecated and will be '
                    'removed in a future version of Django-Flags. '
                    'Please use a list of dicts or tuples instead.',
                    FutureWarning,
                )
                conditions = conditions.items()

            # Flag conditions should be a list of either 3-tuples of
            # dictionaries in the form (condition, value, required) or
            # {'name': 'condition', 'value': value, 'required': True}
            # but contiune to support 2-tuples for unrequired conditions.
            flags[flag] = []
            for c in conditions:
                # {'name': 'condition', 'value': value, 'required': True}
                if isinstance(c, dict):
                    condition = Condition(
                        c['condition'],
                        c['value'],
                        required=c.get('required', False)
                    )

                # (condition, value, required)
                elif len(c) == 3:
                    condition = Condition(c[0], c[1], required=c[2])

                # (condition, value)
                else:
                    condition = Condition(c[0], c[1], required=False)

                flags[flag].append(condition)

        return flags


class DatabaseCondition(Condition):
    """ Condition that includes the FlagState database object """

    def __init__(self, condition, value, required=False, obj=None):
        super(DatabaseCondition, self).__init__(
            condition, value, required=required
        )
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
                o.condition, o.value, required=o.required, obj=o
            ))
        return flags


def get_flags(sources=None, ignore_errors=False):
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

        try:
            source_flags = source_obj.get_flags()
        except Exception:
            if ignore_errors:
                continue
            else:
                raise

        for flag, conditions in source_flags.items():
            if flag in flags:
                flags[flag].conditions += conditions
            else:
                flags[flag] = Flag(flag, conditions)

    return flags
