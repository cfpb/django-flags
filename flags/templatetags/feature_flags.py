from django import template

from flags.state import (
    flag_enabled as base_flag_enabled,
    flag_disabled as base_flag_disabled
)


register = template.Library()


# @register.simple_tag(takes_context=True)
@register.assignment_tag(takes_context=True)
def flag_enabled(context, flag_name):
    request = context['request']
    return base_flag_enabled(flag_name, request=request)


# @register.simple_tag(takes_context=True)
@register.assignment_tag(takes_context=True)
def flag_disabled(context, flag_name):
    request = context['request']
    return base_flag_disabled(flag_name, request=request)
