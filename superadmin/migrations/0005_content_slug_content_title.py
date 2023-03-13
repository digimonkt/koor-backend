# Generated by Django 4.1.5 on 2023-03-06 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0004_content_delete_privacypolicy_delete_userrights'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='slug',
            field=models.SlugField(blank=True, db_column='slug', null=True, unique=True),
        ),
        migrations.AddField(
            model_name='content',
            name='title',
            field=models.CharField(db_column='title', default='', max_length=255, verbose_name='Title'),
            preserve_default=False,
        ),
    ]