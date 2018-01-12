# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-13 00:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FiNote_API', '0011_auto_20180112_2329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dvdfav',
            name='movie_user',
        ),
        migrations.RemoveField(
            model_name='movieuseronomatopoeia',
            name='movie_user',
        ),
        migrations.RemoveField(
            model_name='movieuseronomatopoeia',
            name='onomatopoeia',
        ),
        migrations.AddField(
            model_name='movie_user',
            name='dvd',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie_user',
            name='fav',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie_user',
            name='onomatopoeia',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='FiNote_API.Onomatopoeia'),
        ),
        migrations.AddField(
            model_name='movie_user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='DVDFAV',
        ),
        migrations.DeleteModel(
            name='MovieUserOnomatopoeia',
        ),
    ]
