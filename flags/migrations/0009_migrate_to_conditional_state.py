# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards(apps, schema_editor):
    """ Populate the new name, condition, and value fields on FlagState from
    old Flag and FlagState fields """
    FlagState = apps.get_model('flags', 'FlagState')

    for state in FlagState.objects.all():
        state.name = state.flag.key
        state.condition = 'site'
        state.value = "{hostname}:{port}".format(
            hostname=state.site.hostname, port=state.site.port)
        state.save()


def backwards(apps, schema_editor):
    """ Populate Flag and FlagState foreign keys from new FlagState fields """
    Flag = apps.get_model('flags', 'Flag')
    FlagState = apps.get_model('flags', 'FlagState')
    Site = apps.get_model('wagtailcore', 'Site')

    for state in FlagState.objects.all():
        flag = Flag.objects.create(key=state.name)
        state.flag = flag

        if ':' not in state.value:
            state.value += ':80'
        hostname, port = state.value.split(':')
        site = Site.objects.get(hostname=hostname, port=port)
        state.site = site

        state.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0008_add_state_conditions'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
