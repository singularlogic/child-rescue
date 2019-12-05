# Generated by Django 2.1.5 on 2019-07-22 10:24

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Alert",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "geolocation_point",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=4326
                    ),
                ),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("address", models.CharField(blank=True, max_length=500, null=True)),
                ("radius", models.FloatField(default=5.0)),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=5000, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        )
    ]