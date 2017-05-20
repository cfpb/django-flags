from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from flags.decorators import flag_check
from flags.forms import FlagStateForm
from flags.models import FlagState
from flags.settings import get_flags


def index(request):
    flags = OrderedDict(sorted(get_flags().items(), key=lambda x: x[0]))
    context = {
        'flag_states': FlagState.objects.all(),
        'flags': flags,
    }
    return render(request, 'flagadmin/index.html', context)


def create(request):
    if request.method == 'POST':
        form = FlagStateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flagadmin:list')
    else:
        form = FlagStateForm()

    context = dict(form=form)
    return render(request, 'flagadmin/flags/create.html', context)


def delete(request, state_id):
    flag_state = get_object_or_404(FlagState, pk=state_id)

    if request.method == 'POST':
        flag_state.delete()
        return redirect('flagadmin:list')

    context = dict(state_str=str(flag_state), state_id=flag_state.pk)
    return render(request, 'flagadmin/flags/delete.html', context)


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
