# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-16 22:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodadmin', '0006_stockpick_enddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockpick',
            name='EndDate',
            field=models.DateField(default=datetime.date(2018, 6, 16)),
        ),
        migrations.AlterField(
            model_name='stockpick',
            name='PickDate',
            field=models.DateField(default=datetime.date(2018, 6, 16)),
        ),
    ]