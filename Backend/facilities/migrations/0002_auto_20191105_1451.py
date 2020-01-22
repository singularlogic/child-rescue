# Generated by Django 2.1.5 on 2019-11-05 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("facilities", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="facility", name="geolocation_point",),
        migrations.AddField(model_name="facility", name="latitude", field=models.FloatField(blank=True, null=True),),
        migrations.AddField(model_name="facility", name="longitude", field=models.FloatField(blank=True, null=True),),
        migrations.AlterField(model_name="facility", name="name", field=models.CharField(max_length=128),),
        migrations.AlterField(
            model_name="facility", name="supports_hosting", field=models.BooleanField(default=False),
        ),
    ]
