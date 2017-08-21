# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_auto_20170818_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='type_id',
            field=models.CharField(default=b'', max_length=128),
        ),
    ]
