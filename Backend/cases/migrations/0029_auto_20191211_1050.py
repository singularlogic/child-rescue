# Generated by Django 2.1.5 on 2019-12-11 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0028_auto_20191206_1422"),
    ]

    operations = [
        migrations.CreateModel(
            name="SocialMedia",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("medium", models.CharField(blank=True, max_length=120, null=True)),
                (
                    "published_photos",
                    models.CharField(
                        blank=True,
                        choices=[("yes", "Yes"), ("no", "No"), (None, "Unknown")],
                        default=None,
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "followers",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("low", "Low < 50"),
                            ("medium", "Medium < 500"),
                            ("high", "High < 3000"),
                            ("influencer", "Influencer < 10000"),
                            (None, "Unknown"),
                        ],
                        default=None,
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "recent_activity",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("daily", "Daily"),
                            ("frequently", "Frequently"),
                            ("infrequent", "Infrequent"),
                            ("inactive", "Inactive"),
                            (None, "Unknown"),
                        ],
                        default=None,
                        max_length=20,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name_plural": "social_media", "db_table": "social_media",},
        ),
        migrations.RemoveField(model_name="socialmediadata", name="case",),
        migrations.AlterField(
            model_name="case",
            name="addiction",
            field=models.CharField(
                blank=True, choices=[("yes", "Yes"), ("no", "No"), (None, "Unknown")], max_length=30, null=True
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="body_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("slim", "Slim"),
                    ("normal", "Normal"),
                    ("overweight", "Overweight"),
                    ("corpulent", "Corpulent"),
                    (None, "Unknown"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="education_level",
            field=models.CharField(
                blank=True,
                choices=[
                    ("first_grade", "1st Grade"),
                    ("second_grade", "2st Grade"),
                    ("third_grade", "3st Grade"),
                    (None, "Unknown"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="has_trafficking_history",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("possibly", "Possibly"), ("no", "No"), (None, "Unknown")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="health_issues",
            field=models.CharField(
                blank=True, choices=[("yes", "Yes"), ("no", "No"), (None, "Unknown")], max_length=30, null=True
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="is_first_time_missing",
            field=models.CharField(
                blank=True, choices=[("yes", "Yes"), ("no", "No"), (None, "Unknown")], max_length=20, null=True
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="is_high_risk",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("possibly", "Possibly"), ("no", "No"), (None, "Unknown")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="is_refugee",
            field=models.CharField(
                blank=True, choices=[("yes", "Yes"), ("no", "No"), (None, "Unknown")], max_length=20, null=True
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="medical_treatment_required",
            field=models.CharField(
                blank=True, choices=[("yes", "Yes"), ("no", "No"), (None, "Unknown")], max_length=30, null=True
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="physical_disabilities",
            field=models.CharField(
                blank=True, choices=[("yes", "Yes"), ("no", "No"), (None, "Unknown")], max_length=30, null=True
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="relationship_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("single", "Single"),
                    ("in_relationship", "In a relationship"),
                    ("complicated", "It's complicated"),
                    ("broke_up", "Recently broke up"),
                    ("other", "Other"),
                    (None, "Unknown"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="school_grades",
            field=models.CharField(
                blank=True,
                choices=[
                    ("excellent", "Excellent"),
                    ("good", "Good"),
                    ("average", "Sufficient"),
                    ("not_good", "Not good"),
                    ("bad", "Bad"),
                    (None, "Unknown"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="skin_color",
            field=models.CharField(
                blank=True,
                choices=[
                    ("light_pale", "Light Pale"),
                    ("pale", "Pale"),
                    ("tanned", "Tanned"),
                    ("brown", "Brown"),
                    ("dark_brown", "Dark Brown"),
                    ("black", "Black"),
                    (None, "Unknown"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="stature",
            field=models.CharField(
                blank=True,
                choices=[("tall", "Tall"), ("short", "Short"), ("normal", "Normal"), (None, "Unknown")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="triggered_event",
            field=models.CharField(
                blank=True, choices=[("yes", "Yes"), ("no", "No"), (None, "Unknown")], max_length=30, null=True
            ),
        ),
        migrations.AlterField(
            model_name="child",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("male", "Male"), ("female", "Female"), (None, "Unknown")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.DeleteModel(name="SocialMediaData",),
        migrations.AddField(
            model_name="socialmedia",
            name="case",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="social_media", to="cases.Case"
            ),
        ),
    ]
