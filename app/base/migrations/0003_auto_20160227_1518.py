# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20160227_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='games/'),
        ),
    ]