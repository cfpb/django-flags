from django import template

from flags.template_functions import (
    flag_enabled as base_flag_enabled,
    flags_enabled as base_flags_enabled,
    flag_disabled as base_flag_disabled
)


register = template.Library()


# @register.simple_tag(takes_context=True)
@register.assignment_tag(takes_context=True)
def flag_enabled(context, key):
    request = context['request']
    return base_flag_enabled(request, key)


# @register.simple_tag(takes_context=True)
@register.assignment_tag(takes_context=True)
def flags_enabled(context, *keys):
    request = context['request']
    return all(base_flags_enabled(request, key) for key in keys)


# @register.simple_tag(takes_context=True)
@register.assignment_tag(takes_context=True)
def flag_disabled(context, key):
    request = context['request']
    return base_flag_disabled(request, key)
