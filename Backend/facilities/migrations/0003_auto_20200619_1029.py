# Generated by Django 2.2.8 on 2020-06-19 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20191105_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
