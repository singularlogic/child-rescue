# Generated by Django 2.2.8 on 2020-07-23 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0046_anonymizedcase_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymizedcase',
            name='amber_alert',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='created_at',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='date_of_birth',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='disappearance_reasons',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='disappearance_type',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='first_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='last_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='nationality',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='organization',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='anonymizedcase',
            name='updated_at',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
