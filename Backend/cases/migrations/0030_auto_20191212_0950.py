# Generated by Django 2.1.5 on 2019-12-12 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0029_auto_20191211_1050"),
    ]

    operations = [
        migrations.AlterField(
            model_name="case",
            name="status",
            field=models.CharField(
                choices=[
                    ("inactive", "Inactive"),
                    ("active", "Active"),
                    ("closed", "Closed"),
                    ("archived", "Archived"),
                ],
                default="active",
                max_length=20,
            ),
        ),
    ]
