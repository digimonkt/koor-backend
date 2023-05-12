# Generated by Django 4.1.5 on 2023-04-03 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_meta', '0007_remove_jobseekercategory_active_and_more'),
        ('user_profile', '0006_userfilters_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfilters',
            name='category',
            field=models.ManyToManyField(blank=True, db_column='category', null=True, related_name='%(app_label)s_%(class)s_category', to='jobs.jobcategory', verbose_name='Category'),
        ),
    ]
