# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0010_auto_20170828_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='articletype',
            name='alias',
            field=models.CharField(default=b'', max_length=256),
        ),
    ]
