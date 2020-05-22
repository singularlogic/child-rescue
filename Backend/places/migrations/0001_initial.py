# Generated by Django 2.1.5 on 2019-11-22 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cases", "0023_remove_feed_title"),
        ("feedbacks", "0005_feedback_score"),
    ]

    operations = [
        migrations.CreateModel(
            name="Place",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=4096, null=True),
                ),
                (
                    "tag",
                    models.CharField(
                        choices=[
                            ("hobby_related", "Hobby related"),
                            ("family_related", "Family related"),
                            ("education_related", "Education related"),
                            ("probable_destination", "Probable destination"),
                            ("checked_in", "Checked-in recently/multiply"),
                            ("social_event", "Social event"),
                            ("fact", "Fact"),
                            ("other", "Other POI"),
                        ],
                        default="other",
                        max_length=128,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[
                            ("testimonials", "Testimonials"),
                            ("facts", "Facts"),
                            ("analytics", "Analytics"),
                            ("social_media", "Social media"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=128,
                    ),
                ),
                ("address", models.CharField(max_length=240)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("radius", models.FloatField(default=5.0)),
                ("evaluation", models.FloatField(default=0.0)),
                ("is_searched", models.BooleanField(default=False)),
                (
                    "case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cases.Case"
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="feedbacks.Feedback",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
