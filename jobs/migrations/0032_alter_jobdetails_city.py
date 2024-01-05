# Generated by Django 4.1.5 on 2023-12-06 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_meta', '0019_alter_choice_slug_alter_city_slug_alter_country_slug_and_more'),
        ('jobs', '0031_alter_jobcategory_slug_alter_jobsubcategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdetails',
            name='city',
            field=models.ForeignKey(blank=True, db_column='city', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_city', to='project_meta.city', verbose_name='City'),
        ),
    ]