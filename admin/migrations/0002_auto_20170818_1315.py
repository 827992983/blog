# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.CharField(max_length=128, serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=64)),
                ('auther', models.CharField(max_length=64)),
                ('htlm_context', models.TextField(default=b'')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='article_id',
            field=models.CharField(default=b'', max_length=128),
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
