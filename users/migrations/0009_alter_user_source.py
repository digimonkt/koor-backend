# Generated by Django 4.1.5 on 2023-03-13 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_user_creation_type_user_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='source',
            field=models.CharField(choices=[('app', 'App'), ('apple', 'Apple'), ('facebook', 'Facebook'), ('google', 'Google')], db_column='source', default='app', max_length=250, verbose_name='Source'),
        ),
    ]
