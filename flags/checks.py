from django.core.checks import Warning, register


@register()
def flag_conditions_check(app_configs, **kwargs):
    from flags.sources import get_flags

    error_str = 'Flag {flag} has non-existent condition "{condition}"'
    error_hint = 'Register "{condition}" as a Django-Flags condition.'

    errors = []

    flags = get_flags(ignore_errors=True)
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
