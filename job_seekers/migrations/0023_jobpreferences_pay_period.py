# Generated by Django 4.1.5 on 2023-07-04 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seekers', '0022_alter_categories_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpreferences',
            name='pay_period',
            field=models.CharField(blank=True, choices=[('yearly', 'Yearly'), ('quarterly', 'Quarterly'), ('monthly', 'Monthly'), ('weekly', 'Weekly'), ('hourly', 'Hourly')], db_column='pay_period', default='monthly', max_length=255, null=True, verbose_name='Pay Period'),
        ),
    ]