# Generated by Django 2.2.8 on 2020-08-03 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firebase', '0002_fcmdevice_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fcmdevice',
            name='type',
            field=models.CharField(choices=[('ios_gr', 'ios_gr'), ('ios_be', 'ios_be'), ('android', 'android'), ('web', 'web')], max_length=10),
        ),
    ]