# Generated by Django 2.1.5 on 2019-08-08 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("cases", "0006_auto_20190808_1318")]

    operations = [
        migrations.AlterField(
            model_name="case",
            name="status",
            field=models.CharField(default="inactive", max_length=20),
        ),
        migrations.AlterField(
            model_name="medicaldata",
            name="health_issues",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="physicaldata",
            name="body_type",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="physicaldata",
            name="eye_color",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="physicaldata",
            name="hair_color",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="physicaldata",
            name="stature",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="psychologicaldata",
            name="relationship_status",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="psychologicaldata",
            name="school_absences",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="psychologicaldata",
            name="school_grades",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]