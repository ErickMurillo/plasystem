# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-02 22:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0007_auto_20170928_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablaingresos',
            name='adjuntar_archivo',
            field=models.FileField(upload_to='documentosIngresos/'),
        ),
    ]
