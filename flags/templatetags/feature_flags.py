import django
from django import template

from flags.state import (
    flag_disabled as base_flag_disabled,
    flag_enabled as base_flag_enabled,
)


register = template.Library()

if django.VERSION >= (1, 9):  # pragma: no cover
    simple_tag = register.simple_tag
else:  # pragma: no cover
    simple_tag = register.assignment_tag


# Creates template tags flag_enabled and flag_disabled that call
# base_flag_enabled and base_flag_disabled, passing in any arguments, including
# the request (which could be passed explicitly, or pulled from the context).


@simple_tag(takes_context=True)
def flag_enabled(context, flag_name, request=None, **kwargs):
    if request is None:
        request = context.get('request')
    return base_flag_enabled(flag_name, request=request, **kwargs)


@simple_tag(takes_context=True)
def flag_disabled(context, flag_name, request=None, **kwargs):
    if request is None:
        request = context.get('request')
    return base_flag_disabled(flag_name, request=request, **kwargs)
