# Generated by Django 2.2.8 on 2020-06-12 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0008_auto_20191219_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='score',
            field=models.FloatField(default=1.0),
        ),
    ]
