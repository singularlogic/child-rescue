# Generated by Django 2.1.5 on 2019-04-10 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0008_auto_20190410_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='psychologicaldata',
            name='school_grades',
            field=models.CharField(blank=True, choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Sufficient'), ('not_good', 'Not good'), ('bad', 'Bad')], max_length=50, null=True),
        ),
    ]
