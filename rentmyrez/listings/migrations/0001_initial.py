# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 05:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('description', models.TextField()),
                ('listing_url', models.CharField(max_length=250, unique=True)),
                ('listing_id', models.IntegerField(unique=True)),
                ('address', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('date_listed', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('date_listed',),
            },
        ),
    ]
