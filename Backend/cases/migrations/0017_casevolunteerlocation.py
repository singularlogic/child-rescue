# Generated by Django 2.1.5 on 2019-11-12 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0016_auto_20191112_1021"),
    ]

    operations = [
        migrations.CreateModel(
            name="CaseVolunteerLocation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "case_volunteer",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="cases.CaseVolunteer"),
                ),
            ],
            options={"db_table": "case_volunteer_location",},
        ),
    ]
