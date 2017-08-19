# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('comment_id', models.CharField(max_length=128, serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=64)),
                ('context', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='AtricleType',
            fields=[
                ('type_id', models.CharField(max_length=128, serialize=False, primary_key=True)),
                ('type_name', models.CharField(max_length=64)),
                ('description', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('real_name', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('role', models.CharField(max_length=64)),
                ('email', models.CharField(default=b'', max_length=64)),
                ('phone', models.CharField(default=b'', max_length=64)),
                ('description', models.CharField(default=b'', max_length=256)),
            ],
        ),
    ]
