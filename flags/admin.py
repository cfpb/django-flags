from django.contrib import admin

from flags.forms import FlagStateForm
from flags.models import FlagState


class FlagStateAdmin(admin.ModelAdmin):
    form = FlagStateForm


admin.site.register(FlagState, FlagStateAdmin)
