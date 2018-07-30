from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView

from flags.decorators import flag_check


class FlaggedViewMixin(object):
    flag_name = None
    fallback = None
    condition = True

    def dispatch(self, request, *args, **kwargs):
        if self.flag_name is None:
            raise ImproperlyConfigured(
                "FlaggedViewMixin requires a 'flag_name' argument."
            )

        super_dispatch = super(FlaggedViewMixin, self).dispatch

        decorator = flag_check(
            self.flag_name,
            self.condition,
            fallback=self.fallback,
        )

        return decorator(super_dispatch)(request, *args, **kwargs)


class FlaggedTemplateView(FlaggedViewMixin, TemplateView):
    pass
