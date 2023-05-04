# Generated by Django 4.1.5 on 2023-05-04 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0026_alter_jobslanguageproficiency_spoken_and_more'),
        ('job_seekers', '0021_alter_appliedjobattachmentsitem_applied_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category',
            field=models.ForeignKey(db_column='category', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_categories', to='jobs.jobsubcategory', verbose_name='Category'),
        ),
    ]