# Generated by Django 2.1.5 on 2019-04-09 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0003_case_default_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographicdata',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demographic_data_case', to='cases.Case'),
        ),
    ]
