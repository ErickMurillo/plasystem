# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-20 20:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0004_auto_20170620_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductosOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.RemoveField(
            model_name='productos',
            name='producto',
        ),
        migrations.AddField(
            model_name='productos',
            name='producto1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='organizaciones.ProductosOrg'),
            preserve_default=False,
        ),
    ]
