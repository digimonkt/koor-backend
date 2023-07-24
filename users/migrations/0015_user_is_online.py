# Generated by Django 4.1.5 on 2023-07-24 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_get_email_user_get_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_online',
            field=models.BooleanField(blank=True, db_column='is_online', default=False, null=True, verbose_name='Is Online'),
        ),
    ]