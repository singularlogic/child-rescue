# Generated by Django 2.2.8 on 2020-10-12 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0009_auto_20200612_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='child_status',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='feedback_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('relevant', 'Relevant'), ('irrelevant', 'Irrelevant'), ('credible', 'Credible'), ('spam', 'Spam')], default='pending', max_length=256),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='transportation',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
