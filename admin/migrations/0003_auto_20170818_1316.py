# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_auto_20170818_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomment',
            name='article_id',
            field=models.CharField(max_length=128),
        ),
    ]
