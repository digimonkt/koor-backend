# Generated by Django 4.1.5 on 2023-04-03 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_seekers', '0017_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpreferences',
            name='user',
            field=models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]