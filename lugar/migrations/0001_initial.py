# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comunidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Comunidades',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name=b'C\xc3\xb3digo')),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(help_text=b'Usado como url unica(autorellenado)', null=True, unique=True)),
                ('extension', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name=b'Extension Territorials')),
                ('latitud', models.FloatField(blank=True, null=True, verbose_name=b'Latitud')),
                ('longitud', models.FloatField(blank=True, null=True, verbose_name=b'Longitud')),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name=b'C\xc3\xb3digo')),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(help_text=b'Usado como url unica(autorellenado)', null=True, unique=True)),
                ('extension', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name=b'Extension Territorial')),
                ('latitud', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True, verbose_name=b'Latitud')),
                ('longitud', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True, verbose_name=b'Longitud')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lugar.Departamento')),
            ],
            options={
                'ordering': ['departamento__nombre', 'nombre'],
                'verbose_name_plural': 'Municipios',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('codigo', models.CharField(help_text=b'C\xc3\xb3digo de 2 letras del pa\xc3\xads, ejemplo : Nicaragua (ni)', max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Pa\xedses',
            },
        ),
        migrations.AddField(
            model_name='departamento',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lugar.Pais'),
        ),
        migrations.AddField(
            model_name='comunidad',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lugar.Municipio'),
        ),
    ]
