# Generated by Django 2.2.8 on 2020-11-04 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0049_auto_20201012_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkedCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linkedcase_case', to='cases.Case')),
                ('linked_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linkedcase_linked_case', to='cases.Case')),
            ],
            options={
                'verbose_name_plural': 'linked-cases',
                'db_table': 'linked-case',
            },
        ),
    ]
