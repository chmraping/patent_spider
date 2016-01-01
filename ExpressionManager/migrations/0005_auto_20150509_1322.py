# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0004_auto_20150504_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expression',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='expression',
            name='name',
            field=models.CharField(max_length=3000, blank=True),
        ),
    ]
