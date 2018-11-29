from django.core.checks import Warning, register
from django.db import ProgrammingError


@register()
def flag_conditions_check(app_configs, **kwargs):
    from flags.sources import get_flags

    error_str = 'Flag {flag} has non-existent condition "{condition}"'
    error_hint = 'Register "{condition}" as a Django-Flags condition.'

    errors = []

    # fetch flags, fail gracefully when the initial migration has
    # not yet been applied
    try:
        flags = get_flags()
    except ProgrammingError:
        return []

    for name, flag in flags.items():
        for condition in flag.conditions:
            if condition.fn is None:
                errors.append(
                    Warning(
                        error_str.format(
                            flag=name, condition=condition.condition
                        ),
                        hint=error_hint.format(
                            condition=condition.condition
                        ),
                        id='flags.E001',
                    )
                )

    return errors
