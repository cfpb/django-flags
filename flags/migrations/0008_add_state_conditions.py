# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0007_unique_flag_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='flagstate',
            name='condition',
            field=models.CharField(default=b'boolean', max_length=64),
        ),
        migrations.AddField(
            model_name='flagstate',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='flagstate',
            name='value',
            field=models.CharField(default=b'True', max_length=127),
        ),
    ]
