# Generated by Django 2.1.5 on 2019-11-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191101_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_geolocation_shared',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_private_account',
        ),
        migrations.RemoveField(
            model_name='user',
            name='postal_code',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=256),
        ),
    ]
