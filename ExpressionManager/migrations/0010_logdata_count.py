# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0009_auto_20150511_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='logdata',
            name='count',
            field=models.CharField(default=1, max_length=100),
        ),
    ]
