# Generated by Django 2.1.5 on 2019-09-05 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("organizations", "0001_initial"), ("alerts", "0002_alert_case")]

    operations = [
        migrations.AddField(
            model_name="alert",
            name="organization",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="organizations.Organization",
            ),
        )
    ]