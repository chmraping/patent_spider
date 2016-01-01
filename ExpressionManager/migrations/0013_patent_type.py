# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0012_auto_20150528_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='patent',
            name='type',
            field=models.CharField(default=b'', max_length=500),
        ),
    ]
