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


def _flag_fn(fn, name):
    @simple_tag(takes_context=True, name=name)
    def wrapped(context, flag_name, request=None, **kwargs):
        if request is None:
            request = context.get('request')
        return fn(flag_name, request=request, **kwargs)

    return wrapped


# Creates template tags flag_enabled and flag_disabled that call
# base_flag_enabled and base_flag_disabled, passing in any arguments, including
# the request (which could be passed explicitly, or pulled from the context).
flag_enabled = _flag_fn(base_flag_enabled, 'flag_enabled')
flag_disabled = _flag_fn(base_flag_disabled, 'flag_disabled')
