# Generated by Django 2.1.5 on 2019-07-22 10:24

import datetime
from django.db import migrations, models
import django.db.models.deletion
import feedbacks.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [("alerts", "0002_alert_case"), ("cases", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Feedback",
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
                ("source", models.CharField(max_length=200)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("current_latitude", models.FloatField(blank=True, null=True)),
                ("current_longitude", models.FloatField(blank=True, null=True)),
                ("comment", models.CharField(blank=True, max_length=8000, null=True)),
                (
                    "feedback_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=feedbacks.utils.FeedbackUtils.feedback_image_path,
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "date",
                    models.DateTimeField(
                        blank=True, default=datetime.datetime.now, null=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("checked_on", models.DateTimeField(blank=True, null=True)),
                (
                    "feedback_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("relevant", "Relevant"),
                            ("irrelevant", "Irrelevant"),
                            ("credible", "Credible"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("is_valid", models.NullBooleanField()),
                (
                    "location_selected_reasons",
                    models.CharField(blank=True, max_length=5000, null=True),
                ),
                (
                    "child_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ok", "Ok"),
                            ("dead", "Dead"),
                            ("initial", "Initial"),
                            ("ill", "Ill"),
                            ("wounded", "Wounded"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "transportation",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("foot", "Foot"),
                            ("bus", "Bus"),
                            ("car", "Car"),
                            ("train", "Train"),
                            ("other", "Other"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "alert",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="alerts.Alert",
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="case",
                        to="cases.Case",
                    ),
                ),
            ],
        )
    ]
