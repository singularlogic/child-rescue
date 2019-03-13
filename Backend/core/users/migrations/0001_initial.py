# Generated by Django 2.1.5 on 2019-02-15 11:32

import core.users.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('role', models.CharField(blank=True, choices=[('admin', 'Administrator'), ('owner', 'Owner'), ('coordinator', 'Coordinator'), ('case_manager', 'Case Manager'), ('network_manager', 'Network Manager'), ('facility_manager', 'Facility Manager')], max_length=20, null=True)),
                ('first_name', models.CharField(blank=True, max_length=256, null=True)),
                ('last_name', models.CharField(blank=True, max_length=256, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('country', models.CharField(blank=True, max_length=250, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=256, null=True)),
                ('is_private_account', models.BooleanField(default=False)),
                ('is_geolocation_shared', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=core.users.utils.profile_image_path)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into the admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_end_user', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Uuid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'uuid',
            },
        ),
        migrations.CreateModel(
            name='UuidActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=30)),
                ('params', models.CharField(blank=True, max_length=1000, null=True)),
                ('device', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Uuid')),
            ],
            options={
                'db_table': 'uuid_activity',
            },
        ),
    ]
