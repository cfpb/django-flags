from flags.state import (
    flag_enabled as base_flag_enabled,
    flag_disabled as base_flag_disabled
)


def flag_enabled(flag_name, request):
    """ Check if a flag is enabled for a given request """
    return base_flag_enabled(flag_name, request=request)


def flag_disabled(flag_name, request):
    """ Check if a flag is disabled for a given request """
    return base_flag_disabled(flag_name, request=request)
