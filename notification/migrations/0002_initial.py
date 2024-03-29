# Generated by Django 4.1.5 on 2024-03-06 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenders', '0001_initial'),
        ('vendors', '0001_initial'),
        ('jobs', '0002_initial'),
        ('notification', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='notification',
            name='job',
            field=models.ForeignKey(blank=True, db_column='job', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_jobs', to='jobs.jobdetails', verbose_name='Job'),
        ),
        migrations.AddField(
            model_name='notification',
            name='job_filter',
            field=models.ForeignKey(blank=True, db_column='job_filter', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_job_filter', to='jobs.jobfilters', verbose_name='Job Filter'),
        ),
        migrations.AddField(
            model_name='notification',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='notification',
            name='tender',
            field=models.ForeignKey(blank=True, db_column='tender', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_tenders', to='tenders.tenderdetails', verbose_name='Tender'),
        ),
        migrations.AddField(
            model_name='notification',
            name='tender_application',
            field=models.ForeignKey(blank=True, db_column='tender_application', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_tender_application', to='vendors.appliedtender', verbose_name='Tender Application'),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
