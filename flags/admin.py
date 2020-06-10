from django.contrib import admin

from flags.forms import FlagMetadataForm, FlagStateForm
from flags.models import FlagMetadata, FlagState


class FlagMetadataAdmin(admin.ModelAdmin):
    form = FlagMetadataForm


class FlagStateAdmin(admin.ModelAdmin):
    form = FlagStateForm


admin.site.register(FlagMetadata, FlagMetadataAdmin)
admin.site.register(FlagState, FlagStateAdmin)
