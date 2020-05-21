from django.core.checks import Warning, register
from django.core.exceptions import ValidationError


@register()
def flag_conditions_check(app_configs, **kwargs):
    from flags.sources import get_flags

    errors = []

    flags = get_flags(ignore_errors=True)
    for name, flag in flags.items():
        for condition in flag.conditions:
            if condition.fn is None:
                errors.append(
                    Warning(
                        (
                            f"Flag {name} has non-existent condition "
                            f"'{condition.condition}'."
                        ),
                        hint=(
                            f"Register '{condition.condition}' as a "
                            "Django-Flags condition."
                        ),
                        id="flags.E001",
                    )
                )
            elif condition.fn.validate is not None:
                try:
                    condition.fn.validate(condition.value)
                except ValidationError as e:
                    errors.append(
                        Warning(
                            (
                                f"Flag {name}'s '{condition.condition}' "
                                "condition has an invalid value."
                            ),
                            hint=e.message,
                            id="flags.E002",
                        )
                    )

    return errors
