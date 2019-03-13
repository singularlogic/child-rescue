# Generated by Django 2.1.5 on 2019-02-15 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('area_of_disappearance', models.CharField(blank=True, max_length=1024, null=True)),
                ('latitude_of_disappearance', models.FloatField(blank=True, null=True)),
                ('longitude_of_disappearance', models.FloatField(blank=True, null=True)),
                ('disappearance_date', models.DateTimeField(blank=True, null=True)),
                ('found_date', models.DateTimeField(blank=True, null=True)),
                ('conditions_of_disappearance', models.CharField(blank=True, max_length=5000, null=True)),
                ('reasons_of_disappearance', models.CharField(blank=True, max_length=5000, null=True)),
                ('child_state', models.CharField(blank=True, choices=[('abused', 'Abused'), ('shocked', 'Shocked'), ('normal', 'Normal'), ('dead', 'Dead'), ('wounded', 'Wounded')], max_length=20, null=True)),
                ('has_mobile_phone', models.BooleanField(default=False)),
                ('has_money_or_credit', models.BooleanField(default=False)),
                ('has_area_knowledge', models.BooleanField(default=False)),
                ('rescue_teams_utilized', models.BooleanField(default=False)),
                ('volunteers_utilized', models.BooleanField(default=False)),
                ('transit_country', models.CharField(blank=True, max_length=1000, null=True)),
                ('arrival_at_facility_date', models.DateTimeField(blank=True, null=True)),
                ('disappearance_type', models.CharField(blank=True, choices=[('runaway', 'Runaway'), ('parental', 'Parental'), ('abduction', 'Abduction'), ('criminal', 'Criminal'), ('missing', 'Missing'), ('minor', 'Minor'), ('tracing', 'Tracing'), ('request', 'Request'), ('unclear', 'Unclear')], max_length=20, null=True)),
                ('multi_times_case', models.IntegerField(blank=True, null=True)),
                ('family_members', models.IntegerField(blank=True, null=True)),
                ('probable_destinations', models.CharField(blank=True, max_length=5000, null=True)),
                ('clothing_with_scent', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'cases',
                'db_table': 'case',
            },
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'children',
                'db_table': 'child',
            },
        ),
        migrations.CreateModel(
            name='DemographicData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('home_address', models.CharField(blank=True, max_length=250, null=True)),
                ('home_country', models.CharField(blank=True, max_length=250, null=True)),
                ('home_postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('home_city', models.CharField(blank=True, max_length=256, null=True)),
                ('birth_address', models.CharField(blank=True, max_length=250, null=True)),
                ('birth_country', models.CharField(blank=True, max_length=250, null=True)),
                ('birth_postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('birth_city', models.CharField(blank=True, max_length=256, null=True)),
                ('education_level', models.CharField(blank=True, choices=[('first_grade', '1st Grade'), ('second_grade', '2st Grade'), ('third_grade', '3st Grade'), ('unknown', 'Unknown')], max_length=20, null=True)),
                ('languages_spoken', models.IntegerField(blank=True, null=True)),
                ('nationality', models.CharField(blank=True, max_length=1024, null=True)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')], max_length=20, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demographic_data', to='cases.Case')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Child')),
            ],
            options={
                'verbose_name_plural': 'demographic_data',
                'db_table': 'demographic_data',
            },
        ),
        migrations.CreateModel(
            name='MedicalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('health_issues', models.CharField(blank=True, max_length=2048, null=True)),
                ('medical_treatment_required', models.BooleanField(default=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Child')),
            ],
            options={
                'verbose_name_plural': 'medical_data',
                'db_table': 'medical_data',
            },
        ),
        migrations.CreateModel(
            name='PhysicalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('eye_color', models.CharField(blank=True, max_length=50, null=True)),
                ('hair_color', models.CharField(blank=True, max_length=50, null=True)),
                ('skin_color', models.CharField(blank=True, max_length=50, null=True)),
                ('height', models.CharField(blank=True, max_length=50, null=True)),
                ('weight', models.CharField(blank=True, max_length=50, null=True)),
                ('stature', models.CharField(blank=True, choices=[('tall', 'Tall'), ('short', 'Short'), ('normal', 'Normal')], max_length=20, null=True)),
                ('body_type', models.CharField(blank=True, choices=[('fat', 'Fat'), ('slim', 'Slim'), ('normal', 'Normal')], max_length=20, null=True)),
                ('characteristics', models.CharField(blank=True, max_length=5000, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Child')),
            ],
            options={
                'verbose_name_plural': 'physical_data',
                'db_table': 'physical_data',
            },
        ),
        migrations.CreateModel(
            name='ProfileData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=50, null=True)),
                ('father_name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('mobile_mother', models.CharField(blank=True, max_length=15, null=True)),
                ('mobile_father', models.CharField(blank=True, max_length=15, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Child')),
            ],
            options={
                'verbose_name_plural': 'profile_data',
                'db_table': 'profile_data',
            },
        ),
        migrations.CreateModel(
            name='SocialData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('social_media', models.CharField(blank=True, max_length=2048, null=True)),
                ('concern', models.CharField(blank=True, choices=[('child_headed_household', 'Child headed household'), ('disabled', 'Disabled'), ('medical_case', 'Medical case'), ('street_child', 'Street child')], max_length=20, null=True)),
                ('psychology', models.CharField(blank=True, choices=[('antisocial', 'Antisocial'), ('suicidal', 'Suicidal'), ('autistic', 'Autistic'), ('depressive', 'Depressive')], max_length=20, null=True)),
                ('family', models.CharField(blank=True, choices=[('both_parents', 'Both parents'), ('mother', 'Mother'), ('father', 'Father'), ('no_parents', 'No parents')], max_length=20, null=True)),
                ('parents_profile', models.CharField(blank=True, choices=[('excellent', 'Excellent'), ('good', 'Good'), ('sufficient', 'Sufficient'), ('not_good', 'Not good'), ('really_bad', 'Really bad')], max_length=20, null=True)),
                ('school_grades', models.CharField(blank=True, max_length=2048, null=True)),
                ('school_absences', models.CharField(blank=True, max_length=2048, null=True)),
                ('hobbies', models.CharField(blank=True, max_length=2048, null=True)),
                ('relationship_status', models.CharField(blank=True, max_length=2048, null=True)),
                ('religion', models.CharField(blank=True, max_length=2048, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Child')),
            ],
            options={
                'verbose_name_plural': 'social_data',
                'db_table': 'social_data',
            },
        ),
        migrations.AddField(
            model_name='case',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Child'),
        ),
    ]
