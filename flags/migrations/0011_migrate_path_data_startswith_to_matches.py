# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

# Before this migration, it was assumed that the value of the `path`
# condition matched from the start of the requested path. Now, a regex
# can be specified to get as crazy as you want with your matching.


def forwards(apps, schema_editor):
    modify_flags(
        apps,
        from_condition='path',
        to_condition='path matches',
        value_fn=lambda path: '^' + path
    )


def backwards(apps, schema_editor):
    modify_flags(
        apps,
        from_condition='path matches',
        to_condition='path',
        value_fn=lambda path: path.lstrip('^')
    )


def modify_flags(apps, from_condition, to_condition, value_fn):
    FlagState = apps.get_model('flags', 'flagstate')

    for flag_state in FlagState.objects.filter(condition=from_condition):
        flag_state.condition = to_condition
        flag_state.value = value_fn(flag_state.value)
        flag_state.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0010_delete_flag_site_fk'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
