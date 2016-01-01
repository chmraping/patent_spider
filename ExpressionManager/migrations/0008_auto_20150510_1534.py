# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0007_logdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patent',
            name='classify_code',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='patent',
            name='main_classify_code',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='patent',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='patent',
            name='province_code',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='patent',
            name='right_demand',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='patent',
            name='state_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='setting',
            name='patent_num',
            field=models.CharField(max_length=300),
        ),
    ]
