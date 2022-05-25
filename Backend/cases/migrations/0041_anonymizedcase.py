# Generated by Django 2.2.8 on 2020-07-21 14:49

import cases.utils
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0040_auto_20200703_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymizedCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_fullname', models.CharField(blank=True, max_length=50, null=True)),
                ('father_fullname', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), (None, 'Unknown')], max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('organization', models.IntegerField()),
                ('case_id', models.IntegerField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('custom_name', models.CharField(blank=True, max_length=100, null=True)),
                ('presence_status', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(default='active', max_length=20)),
                ('arrival_at_facility_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(blank=True, max_length=5000, null=True)),
                ('default_message', models.CharField(blank=True, max_length=5000, null=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to=cases.utils.CaseUtils.case_image_path)),
                ('has_mobile_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('has_money_or_credit', models.CharField(blank=True, max_length=20, null=True)),
                ('has_area_knowledge', models.CharField(blank=True, max_length=20, null=True)),
                ('clothing_with_scent', models.CharField(blank=True, max_length=20, null=True)),
                ('rescue_teams_utilized', models.BooleanField(default=False)),
                ('volunteers_utilized', models.BooleanField(default=False)),
                ('transit_country', models.CharField(blank=True, max_length=1000, null=True)),
                ('disappearance_type', models.CharField(blank=True, max_length=20, null=True)),
                ('amber_alert', models.BooleanField(default=False)),
                ('eye_color', models.CharField(blank=True, max_length=20, null=True)),
                ('hair_color', models.CharField(blank=True, max_length=20, null=True)),
                ('skin_color', models.CharField(blank=True, max_length=50, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('stature', models.CharField(blank=True, max_length=20, null=True)),
                ('body_type', models.CharField(blank=True, max_length=20, null=True)),
                ('haircut', models.CharField(blank=True, max_length=20, null=True)),
                ('characteristics', models.CharField(blank=True, max_length=5000, null=True)),
                ('home_address', models.CharField(blank=True, max_length=250, null=True)),
                ('home_country', models.CharField(blank=True, max_length=250, null=True)),
                ('home_postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('birth_country', models.CharField(blank=True, max_length=250, null=True)),
                ('education_level', models.CharField(blank=True, max_length=20, null=True)),
                ('languages_spoken', models.CharField(blank=True, max_length=250, null=True)),
                ('nationality', models.CharField(blank=True, max_length=1024, null=True)),
                ('addiction', models.CharField(blank=True, max_length=30, null=True)),
                ('health_issues', models.CharField(blank=True, max_length=30, null=True)),
                ('medical_treatment_required', models.CharField(blank=True, max_length=30, null=True)),
                ('health_issues_description', models.CharField(blank=True, max_length=5000, null=True)),
                ('triggered_event', models.CharField(blank=True, max_length=30, null=True)),
                ('concerns', models.CharField(blank=True, max_length=30, null=True)),
                ('mental_disorders', models.CharField(blank=True, max_length=30, null=True)),
                ('psychological_disorders', models.CharField(blank=True, max_length=30, null=True)),
                ('physical_disabilities', models.CharField(blank=True, max_length=30, null=True)),
                ('living_environment', models.CharField(blank=True, max_length=30, null=True)),
                ('family_members', models.IntegerField(blank=True, null=True)),
                ('school_grades', models.CharField(blank=True, max_length=50, null=True)),
                ('hobbies', models.CharField(blank=True, max_length=2048, null=True)),
                ('relationship_status', models.CharField(blank=True, max_length=50, null=True)),
                ('religion', models.CharField(blank=True, max_length=50, null=True)),
                ('disappearance_reasons', models.CharField(blank=True, max_length=30, null=True)),
                ('parents_profile', models.CharField(blank=True, max_length=20, null=True)),
                ('is_high_risk', models.CharField(blank=True, max_length=20, null=True)),
                ('is_first_time_missing', models.CharField(blank=True, max_length=20, null=True)),
                ('has_trafficking_history', models.CharField(blank=True, max_length=20, null=True)),
                ('is_refugee', models.CharField(blank=True, max_length=20, null=True)),
                ('legal_status', models.CharField(blank=True, max_length=20, null=True)),
                ('contacted_date', models.DateField(blank=True, null=True)),
                ('risk_indicator', models.FloatField(default=0.0)),
                ('days_diff', models.FloatField(default=0.0)),
                ('go_missing_possibility', models.FloatField(default=0.0)),
                ('current_mindset', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name_plural': 'anonymized_case',
                'db_table': 'anonymized_case',
            },
        ),
    ]