# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0002_setting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='scrap_date',
        ),
        migrations.AddField(
            model_name='setting',
            name='scrap_delay',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
