# Generated by Django 4.1.5 on 2024-05-31 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('applied', 'Applied'), ('applied_tender', 'Applied Tender'), ('password_update', 'Password Updated'), ('shortlisted', 'Shortlisted'), ('rejected', 'Rejected'), ('planned_interviews', 'Planned Interviews'), ('message', 'Message'), ('advance_filter', 'Advance Filter'), ('job_preference', 'Job Preference'), ('expired_save_job', 'Expired Save Job'), ('message', 'Message')], db_column='nitification_type', max_length=25, verbose_name='Notification Type'),
        ),
    ]