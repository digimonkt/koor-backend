# Generated by Django 4.1.5 on 2024-06-03 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_alter_notification_notification_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='active',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='is_removed',
        ),
    ]
