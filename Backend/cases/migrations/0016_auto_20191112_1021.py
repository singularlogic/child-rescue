# Generated by Django 2.1.5 on 2019-11-12 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0015_auto_20191111_1409"),
    ]

    operations = [
        migrations.AlterField(
            model_name="casevolunteer", name="has_accept_invitation", field=models.NullBooleanField(default=None),
        ),
    ]
