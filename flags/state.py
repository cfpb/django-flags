from django.apps import apps
from django.core.exceptions import AppRegistryNotReady

from flags.sources import get_flags


def _get_flag_state(flag_name, **kwargs):
    """A private function that performs the actual state checking"""
    flags = get_flags(request=kwargs.get("request"))

    flag = flags.get(flag_name)
    if flag is not None:
        return flag.check_state(**kwargs)

    return None


def _set_flag_state(
    flag_name, state, create_boolean_condition=True, request=None
):
    """A private function to set a boolean condition to the desired state"""
    from flags.models import FlagState

    flags = get_flags(request=request)
    flag = flags.get(flag_name)
    if flag is None:
        raise KeyError(f"No flag with name {flag_name} exists")

    db_boolean_condition = next(
        (
            c
            for c in flag.conditions
            if c.condition == "boolean" and getattr(c, "obj", None) is not None
        ),
        None,
    )

    if db_boolean_condition is not None:
        # We already have a boolean condition
        boolean_condition_obj = db_boolean_condition.obj
    elif db_boolean_condition is None and create_boolean_condition:
        # We can create a boolean condition and we need to.
        boolean_condition_obj = FlagState(
            name=flag_name, condition="boolean", value="True"
        )
    else:
        raise ValueError(f"Flag {flag_name} does not have a boolean condition")

    boolean_condition_obj.value = state
    boolean_condition_obj.save()


def flag_state(flag_name, **kwargs):
    """Return the value for the flag by passing kwargs to its conditions"""
    if not apps.ready:
        raise AppRegistryNotReady(
            "Feature flag state cannot be checked before the app registry "
            "is ready."
        )

    return _get_flag_state(flag_name, **kwargs)


def flag_enabled(flag_name, **kwargs):
    """Check if a flag is enabled by passing kwargs to its conditions."""
    return flag_state(flag_name, **kwargs)


def flag_disabled(flag_name, **kwargs):
    """Check if a flag is disabled by passing kwargs to its conditions."""
    return not flag_state(flag_name, **kwargs)


def enable_flag(flag_name, create_boolean_condition=True, request=None):
    """Add or set a boolean condition to `True`"""
    _set_flag_state(
        flag_name,
        True,
        create_boolean_condition=create_boolean_condition,
        request=request,
    )


def disable_flag(flag_name, create_boolean_condition=True, request=None):
    """Add or set a boolean condition to `False`"""
    _set_flag_state(
        flag_name,
        False,
        create_boolean_condition=create_boolean_condition,
        request=request,
    )
