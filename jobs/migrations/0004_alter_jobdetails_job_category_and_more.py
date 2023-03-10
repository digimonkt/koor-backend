# Generated by Django 4.1.5 on 2023-02-13 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_meta', '0003_country_educationlevel_language_skill_city'),
        ('jobs', '0003_jobattachmentsitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdetails',
            name='job_category',
            field=models.ManyToManyField(db_column='job_category', related_name='%(app_label)s_%(class)s_job_category', to='jobs.jobcategory', verbose_name='Job Category'),
        ),
        migrations.AlterField(
            model_name='jobdetails',
            name='language',
            field=models.ManyToManyField(blank=True, db_column='language', null=True, related_name='%(app_label)s_%(class)s_language', to='project_meta.language', verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='jobdetails',
            name='skill',
            field=models.ManyToManyField(db_column='skill', related_name='%(app_label)s_%(class)s_skill', to='project_meta.skill', verbose_name='Skill'),
        ),
    ]
