# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0010_logdata_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='history_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_time', models.DateTimeField(auto_now=True, null=True)),
                ('work_time', models.CharField(max_length=100)),
                ('start_day', models.CharField(max_length=100)),
                ('end_day', models.CharField(max_length=100)),
                ('start_id', models.CharField(default=1, max_length=100)),
                ('end_id', models.CharField(max_length=100)),
                ('state', models.CharField(default=b'\xe5\xa4\xb1\xe8\xb4\xa5', max_length=100)),
            ],
        ),
    ]
