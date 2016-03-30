# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0009_auto_20160327_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='group',
            name='forum_url',
            field=models.URLField(blank=True),
        ),
    ]
