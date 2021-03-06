# Generated by Django 2.1.5 on 2019-12-06 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0027_case_custom_name"),
    ]

    operations = [
        migrations.RemoveField(model_name="demographicdata", name="case",),
        migrations.RemoveField(model_name="medicaldata", name="case",),
        migrations.RemoveField(model_name="personaldata", name="case",),
        migrations.RemoveField(model_name="physicaldata", name="case",),
        migrations.RemoveField(model_name="psychologicaldata", name="case",),
        migrations.AlterModelOptions(
            name="facilityhistory", options={"verbose_name_plural": "facility_history"},
        ),
        migrations.AlterModelOptions(
            name="facilityreport", options={"verbose_name_plural": "facility_reports"},
        ),
        migrations.AlterModelOptions(
            name="feed", options={"verbose_name_plural": "feed"},
        ),
        migrations.AlterModelOptions(
            name="file", options={"verbose_name_plural": "file"},
        ),
        migrations.RenameField(
            model_name="case",
            old_name="probable_destinations",
            new_name="characteristics",
        ),
        migrations.RenameField(
            model_name="case",
            old_name="organizations_cooperated",
            new_name="family_members",
        ),
        migrations.RemoveField(model_name="socialmediadata", name="description",),
        migrations.RemoveField(
            model_name="socialmediadata", name="has_social_profiles",
        ),
        migrations.AddField(
            model_name="case",
            name="addiction",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="arrival_at_facility_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="birth_country",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="body_type",
            field=models.CharField(
                blank=True,
                choices=[("fat", "Fat"), ("slim", "Slim"), ("normal", "Normal")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="concerns",
            field=models.CharField(
                blank=True,
                choices=[
                    ("parent_separation", "Recent separation of parents"),
                    ("on_migration", "On Migration"),
                    (
                        "parents_in_dispute",
                        "Parents in dispute (at court or otherwise)",
                    ),
                    ("physical_sexual_abuse", "Physical or Sexual abuse"),
                    ("death_of_family_member", "Recent death of family member/friend"),
                    ("possibly", "Possibly"),
                    ("none", "None"),
                    (None, "Unknown"),
                ],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="contacted_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="current_mindset",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="case", name="days_diff", field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="case",
            name="disappearance_reasons",
            field=models.CharField(
                blank=True,
                choices=[
                    ("family_issues", "Family Issues"),
                    ("personal_issues", "Personal Issues"),
                    ("love_affair", "Love affair"),
                    ("health_issues", "Health issues"),
                    ("mass_disaster", "Mass disaster"),
                    ("migration", "Migration"),
                    ("other", "Other"),
                    (None, "Unknown"),
                ],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="education_level",
            field=models.CharField(
                blank=True,
                choices=[
                    ("first_grade", "1st Grade"),
                    ("second_grade", "2st Grade"),
                    ("third_grade", "3st Grade"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="eye_color",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="go_missing_possibility",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="case",
            name="hair_color",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="haircut",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="has_trafficking_history",
            field=models.CharField(
                blank=True,
                choices=[
                    ("yes", "Yes"),
                    ("possibly", "Possibly"),
                    ("no", "No"),
                    ("unknown", "Unknown"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="health_issues",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="health_issues_description",
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="height",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="hobbies",
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="home_address",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="home_country",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="home_postal_code",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="is_first_time_missing",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="is_high_risk",
            field=models.CharField(
                blank=True,
                choices=[
                    ("yes", "Yes"),
                    ("possibly", "Possibly"),
                    ("no", "No"),
                    ("unknown", "Unknown"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="is_refugee",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="languages_spoken",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="legal_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("illegal", "No papers/Illegal"),
                    ("temp_papers", "Temporal papers"),
                    ("asylum_granted", "Asylum granted"),
                    ("asylum_applied", "Asylum applied"),
                    ("legal", "Legal"),
                    (None, "Unknown"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="living_environment",
            field=models.CharField(
                blank=True,
                choices=[
                    ("single_bio_parent", "Living with 1 biological parent"),
                    ("both_bio_parents", "Living with both biological parents"),
                    (
                        "bio_step_parents",
                        "Living with 1 biological parent + 1 step-parent",
                    ),
                    ("facility", "Living in camp/hosting facility"),
                    ("relatives", "Living under relatives' care/foster family"),
                    ("institution", "Living in institution /psychiatric facility"),
                    ("transit", "In transit"),
                    (None, "Unknown"),
                ],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="medical_treatment_required",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="mental_disorders",
            field=models.CharField(
                blank=True,
                choices=[
                    ("mild", "Mild"),
                    ("moderate", "Moderate"),
                    ("severe", "Severe, self-threatening"),
                    ("none", "None"),
                    (None, "Unknown"),
                ],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="nationality",
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="parents_profile",
            field=models.CharField(
                blank=True,
                choices=[
                    ("father_step_father", "Father/Stepfather"),
                    ("mother_stepmother", "Mother/Stepmother"),
                    ("both", "Both"),
                    ("none", "None"),
                    (None, "Unknown"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="physical_disabilities",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="psychological_disorders",
            field=models.CharField(
                blank=True,
                choices=[
                    ("mild", "Mild"),
                    ("moderate", "Moderate"),
                    ("severe", "Severe, self-threatening"),
                    ("none", "None"),
                    (None, "Unknown"),
                ],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
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
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="religion",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="risk_indicator",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
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
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
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
                    ("unknown", "Unknown"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="stature",
            field=models.CharField(
                blank=True,
                choices=[("tall", "Tall"), ("short", "Short"), ("normal", "Normal")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="triggered_event",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="weight",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="father_fullname",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="first_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="full_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="gender",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="last_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="mother_fullname",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="socialmediadata",
            name="followers",
            field=models.CharField(
                blank=True,
                choices=[
                    ("low", "Low < 50"),
                    ("medium", "Medium < 500"),
                    ("high", "High < 3000"),
                    ("influencer", "Influencer < 10000"),
                    (None, "Unknown"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="socialmediadata",
            name="medium",
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name="socialmediadata",
            name="published_photos",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="socialmediadata",
            name="recent_activity",
            field=models.CharField(
                blank=True,
                choices=[
                    ("daily", "Daily"),
                    ("frequently", "Frequently"),
                    ("infrequent", "Infrequent"),
                    ("inactive", "Inactive"),
                    (None, "Unknown"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="disappearance_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("runaway", "Runaway"),
                    ("parental_abduction", "Parental Abduction"),
                    ("lost", "Lost, injured or otherwise missing"),
                    ("missing", "Missing UAM"),
                    ("third_party_abduction", "Third-party Abduction"),
                    (None, "Unknown"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="socialmediadata",
            name="case",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="social_media_data",
                to="cases.Case",
            ),
        ),
        migrations.DeleteModel(name="DemographicData",),
        migrations.DeleteModel(name="MedicalData",),
        migrations.DeleteModel(name="PersonalData",),
        migrations.DeleteModel(name="PhysicalData",),
        migrations.DeleteModel(name="PsychologicalData",),
    ]
