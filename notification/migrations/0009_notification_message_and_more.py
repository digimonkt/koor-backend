# Generated by Django 4.1.5 on 2023-07-24 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0008_notification_tender_application_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='message',
            field=models.CharField(blank=True, db_column='message', max_length=255, null=True, verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('applied', 'Applied'), ('applied_tender', 'Applied Tender'), ('password_update', 'Password Updated'), ('shortlisted', 'Shortlisted'), ('planned_interviews', 'Planned Interviews'), ('message', 'Message'), ('advance_filter', 'Advance Filter'), ('expired_save_job', 'Expired Save Job'), ('message', 'Message')], db_column='nitification_type', max_length=25, verbose_name='Notification Type'),
        ),
    ]