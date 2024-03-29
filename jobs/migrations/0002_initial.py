# Generated by Django 4.1.5 on 2024-03-06 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_meta', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobsubcategory',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='jobsubcategory',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='jobslanguageproficiency',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='jobslanguageproficiency',
            name='job',
            field=models.ForeignKey(db_column='job', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_job', to='jobs.jobdetails', verbose_name='Job'),
        ),
        migrations.AddField(
            model_name='jobslanguageproficiency',
            name='language',
            field=models.ForeignKey(db_column='language', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_language', to='project_meta.language', verbose_name='Language'),
        ),
        migrations.AddField(
            model_name='jobslanguageproficiency',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='jobshare',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='jobshare',
            name='job',
            field=models.ForeignKey(db_column='job', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_job', to='jobs.jobdetails', verbose_name='Job'),
        ),
        migrations.AddField(
            model_name='jobshare',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='jobfilters',
            name='city',
            field=models.ForeignKey(blank=True, db_column='city', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_city', to='project_meta.city', verbose_name='City'),
        ),
        migrations.AddField(
            model_name='jobfilters',
            name='country',
            field=models.ForeignKey(blank=True, db_column='country', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_country', to='project_meta.country', verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='jobfilters',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='jobfilters',
            name='job_category',
            field=models.ManyToManyField(blank=True, db_column='job_category', null=True, related_name='%(app_label)s_%(class)s_job_category', to='jobs.jobcategory', verbose_name='Job Category'),
        ),
        migrations.AddField(
            model_name='jobfilters',
            name='job_sub_category',
            field=models.ManyToManyField(blank=True, db_column='job_sub_category', null=True, related_name='%(app_label)s_%(class)s_job_sub_category', to='jobs.jobsubcategory', verbose_name='Job Sub Category'),
        ),
        migrations.AddField(
            model_name='jobfilters',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='jobfilters',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='city',
            field=models.ForeignKey(blank=True, db_column='city', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_city', to='project_meta.city', verbose_name='City'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='company_logo',
            field=models.OneToOneField(blank=True, db_column='company_logo', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_company_logo', to='project_meta.media', verbose_name='Company Logo'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='country',
            field=models.ForeignKey(db_column='country', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_country', to='project_meta.country', verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='highest_education',
            field=models.ForeignKey(blank=True, db_column='highest_education', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_highest_education', to='project_meta.educationlevel', verbose_name='Highest Education'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='job_category',
            field=models.ManyToManyField(db_column='job_category', related_name='%(app_label)s_%(class)s_job_category', to='jobs.jobcategory', verbose_name='Job Category'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='job_sub_category',
            field=models.ManyToManyField(db_column='job_sub_category', related_name='%(app_label)s_%(class)s_job_sub_category', to='jobs.jobsubcategory', verbose_name='Job Sub Category'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='skill',
            field=models.ManyToManyField(blank=True, db_column='skill', null=True, related_name='%(app_label)s_%(class)s_skill', to='project_meta.skill', verbose_name='Skill'),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='user',
            field=models.ForeignKey(blank=True, db_column='user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='jobcategory',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='jobcategory',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='jobattachmentsitem',
            name='attachment',
            field=models.OneToOneField(db_column='attachment', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_attachment', to='project_meta.media', verbose_name='Attachment'),
        ),
        migrations.AddField(
            model_name='jobattachmentsitem',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='jobattachmentsitem',
            name='job',
            field=models.ForeignKey(db_column='job', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_job', to='jobs.jobdetails', verbose_name='Job'),
        ),
        migrations.AddField(
            model_name='jobattachmentsitem',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
    ]
