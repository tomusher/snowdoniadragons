# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 13:42
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(),
        ),
    ]
