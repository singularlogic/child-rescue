# Generated by Django 2.1.5 on 2019-10-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("cases", "0010_case_current_facility_id")]

    operations = [
        migrations.AddField(
            model_name="case",
            name="presence_status",
            field=models.CharField(default="", max_length=20),
        )
    ]
