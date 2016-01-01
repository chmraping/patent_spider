# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='excute_record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_stamp', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='expression',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1000, blank=True)),
                ('content', models.CharField(max_length=3000)),
                ('type', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='patent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apply_number', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('main_classify_code', models.CharField(max_length=100)),
                ('classify_code', models.CharField(max_length=100)),
                ('apply_man', models.TextField()),
                ('invente_man', models.TextField()),
                ('publicity_date', models.CharField(max_length=100)),
                ('publicity_code', models.CharField(max_length=100)),
                ('patent_agent', models.TextField()),
                ('agent', models.TextField()),
                ('aplly_date', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('priority', models.TextField()),
                ('province_code', models.CharField(max_length=50)),
                ('abstract', models.TextField()),
                ('main_right', models.TextField()),
                ('international_apply', models.TextField()),
                ('international_publicity', models.TextField()),
                ('enter_country_date', models.CharField(max_length=100)),
                ('record', models.ForeignKey(to='ExpressionManager.excute_record')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='excute_record',
            name='expression',
            field=models.ForeignKey(to='ExpressionManager.expression'),
            preserve_default=True,
        ),
    ]
