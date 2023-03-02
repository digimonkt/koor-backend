# Generated by Django 4.1.5 on 2023-02-23 17:18

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='smtpsetting',
            name='logo',
            field=models.FileField(db_column='logo', default='/media/test.jpg', unique=True, upload_to=core.models.upload_directory_path, verbose_name='Logo'),
            preserve_default=False,
        ),
    ]