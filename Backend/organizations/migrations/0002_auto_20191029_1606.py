# Generated by Django 2.1.5 on 2019-10-29 16:06

import datetime
from django.db import migrations, models
import organizations.utils


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name_plural': 'organizations'},
        ),
        migrations.AddField(
            model_name='organization',
            name='address',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='organization',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 29, 16, 6, 31, 933701)),
        ),
        migrations.AddField(
            model_name='organization',
            name='description',
            field=models.CharField(default='', max_length=4056),
        ),
        migrations.AddField(
            model_name='organization',
            name='email',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='organization',
            name='facebook',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='organization',
            name='how_to_become_volunteer',
            field=models.CharField(default='', max_length=4056),
        ),
        migrations.AddField(
            model_name='organization',
            name='instagram',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='organization',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=organizations.utils.OrganizationUtils.logo_path),
        ),
        migrations.AddField(
            model_name='organization',
            name='missing_child_actions',
            field=models.CharField(default='', max_length=4056),
        ),
        migrations.AddField(
            model_name='organization',
            name='phone',
            field=models.CharField(default='', max_length=14),
        ),
        migrations.AddField(
            model_name='organization',
            name='twitter',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='organization',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 29, 16, 6, 31, 933720)),
        ),
        migrations.AddField(
            model_name='organization',
            name='website',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterModelTable(
            name='organization',
            table='organization',
        ),
    ]