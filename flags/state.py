from __future__ import absolute_import

from django.apps import apps
from django.core.exceptions import AppRegistryNotReady

from flags.sources import get_flags


def _flag_state(flag_name, **kwargs):
    """ This is a private function that performs the actual state checking """
    flags = get_flags(request=kwargs.get("request"))

    flag = flags.get(flag_name)
    if flag is not None:
        return flag.check_state(**kwargs)

    return None


def flag_state(flag_name, **kwargs):
    """ Return the value for the flag by passing kwargs to its conditions """
    if not apps.ready:
        raise AppRegistryNotReady(
            "Feature flag state cannot be checked before the app registry "
            "is ready."
        )

    return _flag_state(flag_name, **kwargs)


def flag_enabled(flag_name, **kwargs):
    """ Check if a flag is enabled by passing kwargs to its conditions. """
    return flag_state(flag_name, **kwargs)


def flag_disabled(flag_name, **kwargs):
    """ Check if a flag is disabled by passing kwargs to its conditions. """
    return not flag_state(flag_name, **kwargs)
