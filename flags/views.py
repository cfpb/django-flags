import logging
import warnings

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView

from flags.decorators import flag_check


logger = logging.getLogger(__name__)


class FlaggedViewMixin(object):
    flag_name = None
    fallback = None
    state = True

    # condition will be deprecated in a future version, use state instead
    condition = None

    def dispatch(self, request, *args, **kwargs):
        if self.flag_name is None:
            raise ImproperlyConfigured(
                "FlaggedViewMixin requires a 'flag_name' argument."
            )

        if self.condition is not None:
            warnings.warn(
                'condition attribute of FlaggedViewMixin is deprecated and '
                'will be removed in a future version of Django-Flags. '
                'Please use the state attribute instead.',
                FutureWarning,
            )
            self.state = self.condition

        super_dispatch = super(FlaggedViewMixin, self).dispatch

        decorator = flag_check(
            self.flag_name,
            self.state,
            fallback=self.fallback,
        )

        return decorator(super_dispatch)(request, *args, **kwargs)


class FlaggedTemplateView(FlaggedViewMixin, TemplateView):
    pass
