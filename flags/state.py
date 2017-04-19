from flags.settings import get_flags


def flag_state(flag_name, **kwargs):
    """ Return the value for the flag by passing kwargs to its conditions """
    try:
        return get_flags()[flag_name].check_state(**kwargs)
    except KeyError:
        return False


def flag_enabled(flag_name, **kwargs):
    """ Check if a flag is enabled by passing kwargs to its conditions. """
    return flag_state(flag_name, **kwargs)


def flag_disabled(flag_name, **kwargs):
    """ Check if a flag is disabled by passing kwargs to its conditions. """
    return not flag_state(flag_name, **kwargs)
