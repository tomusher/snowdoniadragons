# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 15:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0005_auto_20160227_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='played_games',
        ),
    ]
