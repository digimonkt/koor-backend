# Generated by Django 4.1.5 on 2023-05-29 16:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_alter_chatmessage_attachment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='chat_user',
            field=models.ManyToManyField(db_column='user', related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.DeleteModel(
            name='ConversationUser',
        ),
    ]