# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-20 17:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('CompID', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('StartDate2', models.DateField()),
                ('StartDate', models.DateField()),
                ('Interval', models.IntegerField(default=0)),
                ('EndDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='StockPick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StockTicker', models.CharField(max_length=50)),
                ('PickDate', models.DateField()),
                ('StockPickPrice', models.FloatField(default=0.0)),
                ('CompID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodadmin.Competition')),
                ('IDname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
