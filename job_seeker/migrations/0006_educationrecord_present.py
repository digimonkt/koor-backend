# Generated by Django 4.1.5 on 2023-01-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0005_remove_appliedjob_updated_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationrecord',
            name='present',
            field=models.BooleanField(blank=True, db_column='present', default=True, null=True, verbose_name='Present'),
        ),
    ]
