from django.apps import apps
from django.conf import settings


class SettingsFlagsSource(object):

    def get_flags(self):
        flags = getattr(settings, 'FLAGS', {})
        return flags


class DatabaseFlagsSource(object):

    def get_flags(self):
        flags = {}
        FlagState = apps.get_model('flags', 'FlagState')
        for s in FlagState.objects.all():
            if s.name not in flags:
                flags[s.name] = {}
            flags[s.name][s.condition] = s.value

        return flags
