import warnings

from django.core.exceptions import MiddlewareNotUsed


class FlagConditionsMiddleware:
    def __init__(self, get_response):
        """
        Initialize the response.

        Args:
            self: (todo): write your description
            get_response: (todo): write your description
        """
        warnings.warn(
            "FlagConditionsMiddleware is deprecated and no longer has any "
            "effect. It will be removed in a future version of Django-Flags. ",
            FutureWarning,
        )
        raise MiddlewareNotUsed
