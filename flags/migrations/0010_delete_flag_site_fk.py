# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0009_migrate_to_conditional_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flagstate',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterUniqueTogether(
            name='flagstate',
            unique_together=set([('name', 'condition', 'value')]),
        ),
        migrations.RemoveField(
            model_name='flagstate',
            name='enabled',
        ),
        migrations.RemoveField(
            model_name='flagstate',
            name='flag',
        ),
        migrations.RemoveField(
            model_name='flagstate',
            name='site',
        ),
        migrations.DeleteModel(
            name='Flag',
        ),
    ]
