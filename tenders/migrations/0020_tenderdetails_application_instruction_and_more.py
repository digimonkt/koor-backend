# Generated by Django 4.1.5 on 2023-11-24 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0019_alter_tendercategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenderdetails',
            name='application_instruction',
            field=models.TextField(blank=True, db_column='application_instruction', null=True, verbose_name='Application Instruction'),
        ),
        migrations.AddField(
            model_name='tenderdetails',
            name='apply_through_email',
            field=models.BooleanField(blank=True, db_column='apply_through_email', default=False, null=True, verbose_name='Apply Through Email'),
        ),
        migrations.AddField(
            model_name='tenderdetails',
            name='apply_through_koor',
            field=models.BooleanField(blank=True, db_column='apply_through_koor', default=False, null=True, verbose_name='Apply Through Koor'),
        ),
        migrations.AddField(
            model_name='tenderdetails',
            name='apply_through_website',
            field=models.BooleanField(blank=True, db_column='apply_through_website', default=False, null=True, verbose_name='Apply Through Website'),
        ),
        migrations.AddField(
            model_name='tenderdetails',
            name='cc1',
            field=models.EmailField(blank=True, db_column='cc1', max_length=254, null=True, verbose_name='CC Email 1'),
        ),
        migrations.AddField(
            model_name='tenderdetails',
            name='cc2',
            field=models.EmailField(blank=True, db_column='cc2', max_length=254, null=True, verbose_name='CC Email 2'),
        ),
        migrations.AddField(
            model_name='tenderdetails',
            name='contact_email',
            field=models.EmailField(blank=True, db_column='contact_email', max_length=254, null=True, verbose_name='Contact Email'),
        ),
        migrations.AddField(
            model_name='tenderdetails',
            name='contact_whatsapp',
            field=models.CharField(blank=True, db_column='contact_whatsapp', max_length=15, null=True, verbose_name='Contact Whatsapp'),
        ),
        migrations.AddField(
            model_name='tenderdetails',
            name='website_link',
            field=models.CharField(blank=True, db_column='website_link', max_length=450, null=True, verbose_name='Website Link'),
        ),
    ]