# Generated by Django 4.1.5 on 2024-01-09 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0027_remove_jobseekerprofile_job_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]