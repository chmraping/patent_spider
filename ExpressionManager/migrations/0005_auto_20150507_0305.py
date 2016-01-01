# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0004_auto_20150504_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='patent',
            name='right_demand',
            field=models.CharField(default='none', max_length=4000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patent',
            name='state_code',
            field=models.CharField(default='none', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patent',
            name='valid_state',
            field=models.CharField(default='none', max_length=100),
            preserve_default=False,
        ),
    ]
