# Generated by Django 2.1.5 on 2019-07-22 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("cases", "0001_initial"), ("alerts", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="alert",
            name="case",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="cases.Case"
            ),
        )
    ]
