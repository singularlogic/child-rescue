# Generated by Django 2.1.5 on 2019-11-11 14:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0014_auto_20191108_1115'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='casevolunteer',
            unique_together={('case', 'user')},
        ),
    ]