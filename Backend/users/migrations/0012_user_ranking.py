# Generated by Django 2.1.5 on 2019-11-05 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_user_is_team_leader'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ranking',
            field=models.FloatField(default=0.0),
        ),
    ]
