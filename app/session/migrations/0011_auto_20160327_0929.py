# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0010_auto_20160227_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateTimeField(verbose_name='Session date'),
        ),
    ]