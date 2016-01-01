# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExpressionManager', '0011_history_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='patent',
            name='spider_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='excute_record',
            name='time_stamp',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='expression',
            name='type',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='patent',
            name='aplly_date',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='patent',
            name='apply_number',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='patent',
            name='enter_country_date',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='patent',
            name='publicity_code',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='patent',
            name='publicity_date',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='patent',
            name='state_code',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='patent',
            name='valid_state',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='setting',
            name='patent_num',
            field=models.CharField(max_length=3000),
        ),
    ]
