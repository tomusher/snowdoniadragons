# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 16:53
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20160327_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='data',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]