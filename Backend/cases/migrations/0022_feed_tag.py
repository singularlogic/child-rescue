# Generated by Django 2.1.5 on 2019-11-15 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0021_feed"),
    ]

    operations = [
        migrations.AddField(
            model_name="feed",
            name="tag",
            field=models.CharField(default="general", max_length=128),
        ),
    ]
