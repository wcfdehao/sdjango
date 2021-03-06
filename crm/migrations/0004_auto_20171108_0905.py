# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20171106_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(blank=True, to='crm.Tag'),
        ),
    ]
