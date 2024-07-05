from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _


register = template.Library()


@register.filter
def bool_enabled(flag):
    return any(c.check() for c in flag.conditions if c.condition == "boolean")


@register.filter
def conditions_without_bool(flag):
    return [c for c in flag.conditions if c.condition != "boolean"]


@register.filter
def required_conditions_without_bool(flag):
    return [c for c in conditions_without_bool(flag) if c.required]


@register.filter
def state_str(flag):
    """Construct a string that describes the current state of the flag"""
    non_bool_conditions = conditions_without_bool(flag)
    req_conditions = required_conditions_without_bool(flag)
    bool_conditions = [c for c in flag.conditions if c.condition == "boolean"]
    req_bool_conditions = [c for c in bool_conditions if c.required]

    is_enabled = bool_enabled(flag)

    # Common strings
    enabled_str = _("<b>enabled</b>")
    disabled_str = _("<b>disabled</b>")
    all_requests_str = _("for all requests")
    enabled_all_requests_str = _(" " + enabled_str + " " + all_requests_str)
    disabled_all_requests_str = _(" " + disabled_str + " " + all_requests_str)

    # Start building the state string
    state_str = flag.name + _(" is")

    # If we don't have required boolean conditions, we can rely on is_enabled
    if len(req_bool_conditions) > 0:
        if is_enabled:
            state_str += enabled_all_requests_str
        else:
            state_str += disabled_all_requests_str

    # Otherwise we have to dig into all the non-boolean conditions and figure
    # out what the state string should say
    elif len(non_bool_conditions) > 0:
        # Are there required conditions?
        if len(req_conditions) > 0:
            if (
                len(bool_conditions) > 0
                and len(non_bool_conditions) == len(req_conditions)
                and not is_enabled
            ):
                # state_str += _(' <b>disabled</b> for all requests, even')
                state_str += disabled_all_requests_str
                state_str += _(", even")
            else:
                state_str += " " + enabled_str

            state_str += _(" when <i>all</i> required conditions")

            if len(non_bool_conditions) == len(req_conditions) or is_enabled:
                state_str += _(" are met")

        # If there aren't any required conditions, it's simpler.
        elif is_enabled:
            state_str += " " + enabled_str + _(" for all requests")
        else:
            state_str += " " + enabled_str + _(" when")

        # If there are non-required conditions, we should say something about
        # them too.
        if not is_enabled and len(non_bool_conditions) > len(req_conditions):
            if len(req_conditions) > 0:
                state_str += _(" and")
            state_str += _(" <i>any</i>")
            if len(req_conditions) > 0:
                state_str += _(" non-required")
            state_str += _(" condition is met")

    # Finally, if there are no non-boolean conditions and no required boolean
    # conditions, we can just say it's enabled or disabled for all requests.
    elif is_enabled:
        state_str += enabled_all_requests_str
    else:
        state_str += disabled_all_requests_str

    # Full stop.
    state_str += "."

    return mark_safe(state_str)  # nosec B703, B308
