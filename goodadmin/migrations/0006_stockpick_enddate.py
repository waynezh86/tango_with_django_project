# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-16 22:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('goodadmin', '0005_auto_20180528_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockpick',
            name='EndDate',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]