# Generated by Django 2.1.5 on 2019-11-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_auto_20191101_1149"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="user", name="last_name", field=models.CharField(max_length=256),
        ),
    ]
