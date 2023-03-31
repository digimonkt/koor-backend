# Generated by Django 4.1.5 on 2023-03-29 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_notification_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('applied', 'Applied'), ('password_update', 'Password Updated'), ('shortlisted', 'Shortlisted'), ('message', 'Message'), ('advance_filter', 'Advance Filter'), ('expired_save_job', 'Expired Save Job')], db_column='nitification_type', max_length=25, verbose_name='Notification Type'),
        ),
    ]