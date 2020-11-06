# Generated by Django 2.2.8 on 2020-07-22 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0043_auto_20200721_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='disappearance_type',
            field=models.CharField(blank=True, choices=[('runaway', 'Runaway'), ('parental_abduction', 'Parental Abduction'), ('lost', 'Lost, injured or otherwise missing'), ('missing', 'Missing UAM'), ('third_party_abduction', 'Third-party Abduction'), (None, 'Unknown')], max_length=128, null=True),
        ),
    ]
