import logging

from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string

from flags.conditions import get_condition


logger = logging.getLogger(__name__)


class Condition:
    """A simple wrapper around conditions"""

    def __init__(self, condition, value, required=False):
        self.condition = condition
        self.value = value
        self.fn = get_condition(self.condition)
        self.required = required

    def __eq__(self, other):
        return other.condition == self.condition and other.value == self.value

    def check(self, **kwargs):
        if self.fn is not None:
            return self.fn(self.value, **kwargs)


class Flag:
    """A simple wrapper around feature flags and their conditions"""

    def __init__(self, name, conditions=None):
        if conditions is None:
            conditions = []
        self.name = name
        self.conditions = conditions

    def __eq__(self, other):
        """There can be only one feature flag of a given name"""
        return other.name == self.name

    def check_state(self, **kwargs):
        """Determine this flag's state based on any of its conditions"""
        non_required_conditions = [
            c for c in self.conditions if not c.required
        ]
        required_conditions = [c for c in self.conditions if c.required]

        if len(non_required_conditions) == 0 and len(required_conditions) == 0:
            return False

        checked_conditions = [(c, c.check(**kwargs)) for c in self.conditions]

        state = (
            any(
                state
                for c, state in checked_conditions
                if c in non_required_conditions
            )
            if len(non_required_conditions) > 0
            else True
        ) and (
            all(
                state
                for c, state in checked_conditions
                if c in required_conditions
            )
        )

        if getattr(settings, "FLAGS_STATE_LOGGING", False):
            logger.info(
                "Flag {name} evaluated {state} with "
                "condition{conditions_plural}: {conditions}.".format(
                    name=self.name,
                    state=state,
                    conditions=", ".join(
                        f"{c.condition} ({v})" for c, v in checked_conditions
                    ),
                    conditions_plural="s" if len(self.conditions) > 1 else "",
                )
            )

        return state


class SettingsFlagsSource:
    def get_flags(self):
        settings_flags = getattr(settings, "FLAGS", {}).items()
        flags = {}
        for flag, conditions in settings_flags:
            # Flag conditions should be a list of either 3-tuples of
            # dictionaries in the form (condition, value, required) or
            # {'name': 'condition', 'value': value, 'required': True}
            # but contiune to support 2-tuples for unrequired conditions.
            flags[flag] = []
            for c in conditions:
                # {'name': 'condition', 'value': value, 'required': True}
                if isinstance(c, dict):
                    condition = Condition(
                        c["condition"],
                        c["value"],
                        required=c.get("required", False),
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
    """Condition that includes the FlagState database object"""

    def __init__(self, condition, value, required=False, obj=None):
        super().__init__(condition, value, required=required)
        self.obj = obj


class DatabaseFlagsSource:
    def get_queryset(self):
        FlagState = apps.get_model("flags", "FlagState")
        return FlagState.objects.all()

    def get_flags(self):
        flags = {}
        for o in self.get_queryset():
            if o.name not in flags:
                flags[o.name] = []
            flags[o.name].append(
                DatabaseCondition(
                    o.condition, o.value, required=o.required, obj=o
                )
            )
        return flags


def get_flags(sources=None, ignore_errors=False, request=None):
    """Get all flag sources defined in settings.FLAG_SOURCES.

    FLAG_SOURCES is expected to be a list of Python paths to classes providing
    a get_flags() method that returns a dict with the same format as the
    FLAG setting.

    If a Django request object is provided, it is used as a place to cache
    flag conditions (as request.flag_conditions) or retrieve them if already
    cached on a previous call.
    """
    REQUEST_CACHE_ATTRIBUTE = "flag_conditions"

    if request:
        flags = getattr(request, REQUEST_CACHE_ATTRIBUTE, None)

        if flags:
            return flags

    flags = {}

    if sources is None:
        sources = getattr(
            settings,
            "FLAG_SOURCES",
            (
                "flags.sources.SettingsFlagsSource",
                "flags.sources.DatabaseFlagsSource",
            ),
        )

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

    if request:
        setattr(request, REQUEST_CACHE_ATTRIBUTE, flags)

    return flags
