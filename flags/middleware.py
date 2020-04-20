import warnings


class FlagConditionsMiddleware:
    def __init__(self, get_response):
        warnings.warn(
            "FlagConditionsMiddleware is deprecated and no longer has any "
            "effect. It will be removed in a future version of Django-Flags. ",
            FutureWarning,
        )

    def __call__(self, request):
        pass
