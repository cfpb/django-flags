from django import template

from flags.state import flag_disabled as base_flag_disabled
from flags.state import flag_enabled as base_flag_enabled


register = template.Library()


# Creates template tags flag_enabled and flag_disabled that call
# base_flag_enabled and base_flag_disabled, passing in any arguments, including
# the request (which could be passed explicitly, or pulled from the context).


@register.simple_tag(takes_context=True)
def flag_enabled(context, flag_name, request=None, **kwargs):
    if request is None:
        request = context.get("request")
    return base_flag_enabled(flag_name, request=request, **kwargs)


@register.simple_tag(takes_context=True)
def flag_disabled(context, flag_name, request=None, **kwargs):
    if request is None:
        request = context.get("request")
    return base_flag_disabled(flag_name, request=request, **kwargs)
