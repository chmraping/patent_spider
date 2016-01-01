# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0008_auto_20150510_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excute_record',
            name='time_stamp',
            field=models.CharField(max_length=100),
        ),
    ]
