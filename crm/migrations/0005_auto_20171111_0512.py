# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20171108_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
    ]