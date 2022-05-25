# Generated by Django 2.2.8 on 2020-04-30 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0035_case_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='presence_status',
            field=models.CharField(blank=True, choices=[('present', 'Present'), ('not_present', 'Not present'), ('transit', 'Transit'), ('missing', 'Missing')], default='present', max_length=20, null=True),
        ),
    ]