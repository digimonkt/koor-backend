# Generated by Django 4.1.5 on 2023-04-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_userfilters'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfilters',
            name='availability',
            field=models.BooleanField(blank=True, db_column='availability', null=True, verbose_name='Availability'),
        ),
    ]
