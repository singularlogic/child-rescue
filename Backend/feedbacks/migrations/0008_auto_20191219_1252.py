# Generated by Django 2.2.8 on 2019-12-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feedbacks", "0007_feedback_note"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="feedback_status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("relevant", "Relevant"),
                    ("irrelevant", "Irrelevant"),
                    ("credible", "Credible"),
                    ("spam", "Spam"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
