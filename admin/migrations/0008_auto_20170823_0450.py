# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0007_article_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articletype',
            name='description',
        ),
        migrations.AlterField(
            model_name='articletype',
            name='type_name',
            field=models.CharField(default=b'', max_length=256),
        ),
    ]
