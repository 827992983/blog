# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0005_auto_20170821_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='favorite_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='read_number',
            field=models.IntegerField(default=0),
        ),
    ]
