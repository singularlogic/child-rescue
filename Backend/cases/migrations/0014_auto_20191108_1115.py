# Generated by Django 2.1.5 on 2019-11-08 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0013_remove_case_is_present'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseVolunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_accept_invitation', models.BooleanField(default=False)),
                ('is_team_leader', models.NullBooleanField(default=False)),
                ('team_name', models.CharField(blank=True, max_length=256, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'case_volunteer',
            },
        ),
        migrations.AddField(
            model_name='case',
            name='user',
            field=models.ManyToManyField(through='cases.CaseVolunteer', to=settings.AUTH_USER_MODEL),
        ),
    ]