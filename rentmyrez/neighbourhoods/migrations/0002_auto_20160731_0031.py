# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-31 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neighbourhoods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neighbourhood',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]