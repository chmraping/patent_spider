# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0003_auto_20150428_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='is_scraping',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='setting',
            name='loop',
            field=models.BooleanField(default=False),
        ),
    ]
