# Generated by Django 4.1.5 on 2024-03-19 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_initial'),
        ('superadmin', '0004_userrights_usersubrights_rights'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='job',
            field=models.ForeignKey(blank=True, db_column='job', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_job', to='jobs.jobdetails', verbose_name='Job'),
        ),
    ]