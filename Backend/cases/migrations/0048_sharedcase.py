# Generated by Django 2.2.8 on 2020-08-05 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20191218_1305'),
        ('cases', '0047_auto_20200723_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization')),
            ],
        ),
    ]
