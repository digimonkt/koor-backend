# Generated by Django 4.1.5 on 2023-04-20 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_meta', '0009_allcountry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allcountry',
            name='phone_code',
            field=models.CharField(db_column='phone_code', max_length=50, verbose_name='Phone Code'),
        ),
    ]