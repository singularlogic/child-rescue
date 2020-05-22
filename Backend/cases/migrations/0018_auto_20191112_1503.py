# Generated by Django 2.1.5 on 2019-11-12 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cases", "0017_casevolunteerlocation"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="casevolunteer", options={"verbose_name_plural": "case_volunteers"},
        ),
        migrations.AlterModelOptions(
            name="casevolunteerlocation",
            options={"verbose_name_plural": "case_volunteer_locations"},
        ),
        migrations.AlterModelOptions(
            name="follower", options={"verbose_name_plural": "case_followers"},
        ),
        migrations.AddField(
            model_name="case",
            name="owner",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
