# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0008_auto_20170823_0450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='htlm_context',
            new_name='html_context',
        ),
    ]
