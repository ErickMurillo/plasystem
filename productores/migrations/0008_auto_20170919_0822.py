# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-19 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productores', '0007_auto_20170505_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='SistemaCacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sistema', models.CharField(choices=[('Semilla', 'Semilla'), ('Injerto', 'Injerto'), ('Mixto', 'Mixto')], max_length=50)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productores.Encuesta')),
            ],
        ),
        migrations.AlterField(
            model_name='distribucionfinca',
            name='seleccion',
            field=models.CharField(choices=[('Bosque', 'Bosque'), ('Potrero', 'Potrero'), ('Cultivo anual', 'Cultivo anual'), ('Cultivo asociado', 'Cultivo asociado'), ('Plantaci\xf3n forestal', 'Plantaci\xf3n forestal'), ('Sistema agroforestal', 'Sistema agroforestal'), ('Sistema silvopastoril', 'Sistema silvopastoril'), ('Otros', 'Otros')], max_length=50),
        ),
    ]
