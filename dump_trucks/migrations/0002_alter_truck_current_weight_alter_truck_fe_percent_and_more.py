# Generated by Django 4.2.21 on 2025-06-07 08:29

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.polygon
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dump_trucks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='current_weight',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='truck',
            name='fe_percent',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='truck',
            name='max_capacity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='truck',
            name='sio2_percent',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='unloading',
            name='x',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='unloading',
            name='y',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='current_weight',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='fe_percent',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='polygon',
            field=django.contrib.gis.db.models.fields.PolygonField(default=django.contrib.gis.geos.polygon.Polygon(), srid=4326),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='sio2_percent',
            field=models.FloatField(),
        ),
    ]
