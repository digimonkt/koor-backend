# Generated by Django 4.1.5 on 2024-03-06 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
        ('jobs', '0002_initial'),
        ('project_meta', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorprofile',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='vendorprofile',
            name='license_id_file',
            field=models.OneToOneField(blank=True, db_column='license_id_file', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_license_files', to='project_meta.media', verbose_name='License File'),
        ),
        migrations.AddField(
            model_name='vendorprofile',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='vendorprofile',
            name='organization_type',
            field=models.ManyToManyField(db_column='organization_type', related_name='%(app_label)s_%(class)s_organization_types', to='project_meta.choice', verbose_name='Organization Type'),
        ),
        migrations.AddField(
            model_name='vendorprofile',
            name='registration_certificate',
            field=models.OneToOneField(blank=True, db_column='registration_certificate', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_registration_certificates', to='project_meta.media', verbose_name='Registration Certificate'),
        ),
        migrations.AddField(
            model_name='vendorprofile',
            name='user',
            field=models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_users', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='category',
            field=models.ManyToManyField(blank=True, db_column='category', null=True, related_name='%(app_label)s_%(class)s_category', to='jobs.jobcategory', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='city',
            field=models.ForeignKey(blank=True, db_column='city', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_city', to='project_meta.city', verbose_name='City'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='country',
            field=models.ForeignKey(blank=True, db_column='country', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_country', to='project_meta.country', verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='organization_type',
            field=models.ManyToManyField(blank=True, db_column='organization_type', null=True, related_name='%(app_label)s_%(class)s_organization_types', to='project_meta.choice', verbose_name='Organization Type'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='sector',
            field=models.ManyToManyField(blank=True, db_column='sector', null=True, related_name='%(app_label)s_%(class)s_sector', to='project_meta.choice', verbose_name='Sector'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='sub_category',
            field=models.ManyToManyField(blank=True, db_column='sub_category', null=True, related_name='%(app_label)s_%(class)s_sub_category', to='jobs.jobsubcategory', verbose_name='Sub Category'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='tag',
            field=models.ManyToManyField(blank=True, db_column='tag', null=True, related_name='%(app_label)s_%(class)s_tag', to='project_meta.tag', verbose_name='Tag'),
        ),
        migrations.AddField(
            model_name='userfilters',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='useranalytic',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='reference',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='city',
            field=models.ForeignKey(blank=True, db_column='city', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_city', to='project_meta.city', verbose_name='City'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='country',
            field=models.ForeignKey(blank=True, db_column='country', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_country', to='project_meta.country', verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='highest_education',
            field=models.ForeignKey(blank=True, db_column='highest_education', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_highest_educations', to='project_meta.educationlevel', verbose_name='Highest Education'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='user',
            field=models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='city',
            field=models.ForeignKey(blank=True, db_column='city', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_city', to='project_meta.city', verbose_name='City'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='country',
            field=models.ForeignKey(blank=True, db_column='country', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_country', to='project_meta.country', verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='license_id_file',
            field=models.OneToOneField(blank=True, db_column='license_id_file', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_license_files', to='project_meta.media', verbose_name='License File'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='organization_type',
            field=models.ManyToManyField(db_column='organization_type', related_name='%(app_label)s_%(class)s_organization_types', to='project_meta.choice', verbose_name='Organization Type'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='user',
            field=models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
