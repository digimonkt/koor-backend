# Generated by Django 4.1.5 on 2023-10-18 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_chatmessage_read_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='reply_to',
            field=models.ForeignKey(blank=True, db_column='reply_to', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_reply_to', to='chat.chatmessage', verbose_name='Reply To'),
        ),
    ]
