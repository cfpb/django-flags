from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _


register = template.Library()


@register.filter
def bool_enabled(flag):
    return any(c.check() for c in flag.conditions if c.condition == 'boolean')


@register.filter
def conditions_without_bool(flag):
    return [c for c in flag.conditions if c.condition != 'boolean']


@register.filter
def required_conditions_without_bool(flag):
    return [c for c in conditions_without_bool(flag) if c.required]


@register.filter
def state_str(flag):
    """ Construct a string that describes the current state of the flag """
    non_bool_conditions = conditions_without_bool(flag)
    req_conditions = required_conditions_without_bool(flag)
    bool_conditions = [c for c in flag.conditions if c.condition == 'boolean']
    req_bool_conditions = [c for c in bool_conditions if c.required]

    is_enabled = bool_enabled(flag)

    state_str = flag.name + _(' is')

    if len(req_bool_conditions) > 0:
        if is_enabled:
            state_str += _(' <b>enabled</b> for all requests')
        else:
            state_str += _(' <b>disabled</b> for all requests')

    elif len(non_bool_conditions) > 0:
        if len(req_conditions) > 0:
            state_str += _(' <b>')

            if (len(bool_conditions) > 0 and
                    len(non_bool_conditions) == len(req_conditions) and
                    not is_enabled):
                state_str += _('disabled')
            else:
                state_str += _('enabled')

            state_str += _('</b>')
            state_str += _(' when <i>all</i> required conditions')

            if len(non_bool_conditions) == len(req_conditions):
                state_str += _(' are met')

        elif is_enabled:
            state_str += _(' <b>enabled</b> for all requests')
        else:
            state_str += _(' <b>enabled</b> when')

        if not is_enabled:
            if len(non_bool_conditions) > len(req_conditions):
                if len(req_conditions) > 0:
                    state_str += _(' and')
                state_str += _(' <i>any</i> optional condition is met')

    elif is_enabled:
        state_str += _(' <b>enabled</b> for all requests')
    else:
        state_str += _(' <b>disabled</b> for all requests')

    state_str += '.'

    return mark_safe(state_str)
