# Generated by Django 4.1.5 on 2023-05-24 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0013_remove_tenderdetails_sectors_tenderdetails_sector'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenderdetails',
            name='address',
            field=models.TextField(blank=True, db_column='address', null=True, verbose_name='Address'),
        ),
    ]