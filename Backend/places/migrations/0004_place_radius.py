# Generated by Django 2.2.8 on 2019-12-18 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0003_auto_20191126_1556"),
    ]

    operations = [
        migrations.AddField(model_name="place", name="radius", field=models.FloatField(default=5.0),),
    ]