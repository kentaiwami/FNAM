# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-18 05:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FiNote_API', '0016_auto_20170603_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backup',
            name='add_day',
            field=models.IntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='movie',
            name='overview',
            field=models.TextField(default='', max_length=1000),
        ),
    ]