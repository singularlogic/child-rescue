# Generated by Django 2.2.8 on 2020-07-21 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0041_anonymizedcase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymizedcase',
            name='amber_alert',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='rescue_teams_utilized',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='volunteers_utilized',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
