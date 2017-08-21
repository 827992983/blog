# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0004_article_type_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AtricleType',
            new_name='ArticleType',
        ),
    ]
