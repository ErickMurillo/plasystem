# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 22:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lugar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Actividad',
                'verbose_name_plural': 'Actividades',
            },
        ),
        migrations.CreateModel(
            name='CategoriaGastos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Categoria de gasto',
                'verbose_name_plural': 'Categorias de gatos',
            },
        ),
        migrations.CreateModel(
            name='Componentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Componente',
                'verbose_name_plural': 'Componentes',
            },
        ),
        migrations.CreateModel(
            name='DatosGenerales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_finalizacion', models.DateField()),
                ('responsable', models.CharField(max_length=250, verbose_name='Nombre del responsable')),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsectores.Componentes')),
            ],
            options={
                'verbose_name': 'Dato General (proyecto)',
                'verbose_name_plural': 'Datos Generales (proyectos)',
            },
        ),
        migrations.CreateModel(
            name='GruposMetas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Grupo meta',
                'verbose_name_plural': 'Grupos metas',
            },
        ),
        migrations.CreateModel(
            name='Indicadores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_corto', models.CharField(max_length=25)),
                ('descripcion_completo', models.TextField()),
                ('codigo', models.CharField(max_length=50)),
                ('programatico_mayor', models.FloatField()),
                ('programatico_menor', models.FloatField()),
                ('ejecucion_mayor', models.FloatField()),
                ('ejecucion_menor', models.FloatField()),
            ],
            options={
                'verbose_name': 'Indicador',
                'verbose_name_plural': 'Indicadores',
            },
        ),
        migrations.CreateModel(
            name='Monedas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Tipo moneda',
                'verbose_name_plural': 'Tipos de monedas',
            },
        ),
        migrations.CreateModel(
            name='ObjetivosResultados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objetivo_corto', models.CharField(max_length=25)),
                ('objetivo_completo', models.TextField()),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsectores.DatosGenerales')),
            ],
            options={
                'verbose_name': 'Objectivo de resultado',
                'verbose_name_plural': 'Objectivo de resultados',
            },
        ),
        migrations.CreateModel(
            name='RegistroMeses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.IntegerField(choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')])),
                ('anios', models.IntegerField()),
                ('meta', models.FloatField()),
                ('presupuesto', models.FloatField()),
                ('total_metas', models.FloatField(blank=True, editable=False, null=True)),
                ('total_presupuesto', models.FloatField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Registro de mes',
                'verbose_name_plural': 'Registro de meses',
            },
        ),
        migrations.CreateModel(
            name='RegistroPlanAnual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_financiero', models.CharField(max_length=50)),
                ('tipo_actividad', models.IntegerField(choices=[(1, 'Contribuye'), (2, 'No contribuye')])),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsectores.Actividades')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsectores.CategoriaGastos')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsectores.DatosGenerales')),
            ],
            options={
                'verbose_name': 'Registro plan anual',
                'verbose_name_plural': 'Registros planes anuales',
            },
        ),
        migrations.CreateModel(
            name='TasaCambioPaisAnual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.IntegerField()),
                ('dolar', models.FloatField(default=0)),
                ('euro', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'Tasa de cambio anual',
                'verbose_name_plural': 'Tasas de cambios anuales',
            },
        ),
        migrations.CreateModel(
            name='TipoCambiosMonedaPais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moneda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsectores.Monedas')),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lugar.Pais')),
            ],
            options={
                'verbose_name': 'Tipo de cambio moneda por pais',
                'verbose_name_plural': 'Tipos de cambios monedas por pais',
            },
        ),
        migrations.AddField(
            model_name='tasacambiopaisanual',
            name='tipo_cambio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsectores.TipoCambiosMonedaPais'),
        ),
        migrations.AddField(
            model_name='registromeses',
            name='registro_anual',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsectores.RegistroPlanAnual'),
        ),
        migrations.AddField(
            model_name='indicadores',
            name='objetivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsectores.ObjetivosResultados'),
        ),
        migrations.AddField(
            model_name='datosgenerales',
            name='grupo',
            field=models.ManyToManyField(to='subsectores.GruposMetas'),
        ),
        migrations.AddField(
            model_name='datosgenerales',
            name='moneda',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='pais', chained_model_field='pais', on_delete=django.db.models.deletion.CASCADE, to='subsectores.TipoCambiosMonedaPais'),
        ),
        migrations.AddField(
            model_name='datosgenerales',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lugar.Pais'),
        ),
    ]
