# Generated by Django 2.1.5 on 2019-12-02 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feedbacks", "0005_feedback_score"),
    ]

    operations = [
        migrations.AddField(model_name="feedback", name="is_main", field=models.BooleanField(default=False),),
    ]
