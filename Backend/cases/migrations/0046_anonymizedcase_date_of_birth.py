# Generated by Django 2.2.8 on 2020-07-23 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0045_auto_20200723_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymizedcase',
            name='date_of_birth',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
