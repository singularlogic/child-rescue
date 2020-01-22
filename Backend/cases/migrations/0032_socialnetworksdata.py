# Generated by Django 2.2.8 on 2019-12-19 15:38

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0005_auto_20191218_1305"),
        ("cases", "0031_auto_20191212_1346"),
    ]

    operations = [
        migrations.CreateModel(
            name="SocialNetworksData",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "source",
                    models.CharField(
                        choices=[
                            ("eventful", "Eventful"),
                            ("foursquare", "Foursquare"),
                            ("twitter", "Twitter"),
                            ("google", "Google"),
                            ("other", "Other"),
                        ],
                        default="eventful",
                        max_length=20,
                    ),
                ),
                ("geolocation_point", django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("address", models.CharField(blank=True, max_length=500, null=True)),
                ("city", models.CharField(blank=True, max_length=500, null=True)),
                ("venue", models.CharField(blank=True, max_length=500, null=True)),
                ("description", models.CharField(blank=True, max_length=2000, null=True)),
                ("start", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="cases.Case")),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organizations.Organization",
                    ),
                ),
            ],
        ),
    ]
