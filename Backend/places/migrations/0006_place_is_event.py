# Generated by Django 2.2.8 on 2020-05-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_place_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='is_event',
            field=models.BooleanField(default=False),
        ),
    ]
