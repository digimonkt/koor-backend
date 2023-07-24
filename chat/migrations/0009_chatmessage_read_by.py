# Generated by Django 4.1.5 on 2023-07-20 15:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0008_remove_conversation_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='read_by',
            field=models.ManyToManyField(blank=True, db_column='read_by', null=True, related_name='%(app_label)s_%(class)s_read_by', to=settings.AUTH_USER_MODEL, verbose_name='Read By'),
        ),
    ]