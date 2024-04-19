# Generated by Django 4.1.5 on 2024-04-12 14:14

import core.models
from django.db import migrations, models
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0005_invoice_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceIcon',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('type', models.CharField(choices=[('x', 'X'), ('youtube', 'Youtube'), ('instagram', 'Instagram'), ('linkedin', 'Linkedin'), ('facebook', 'Facebook')], db_column='type', max_length=250, verbose_name='Type')),
                ('icon', models.FileField(db_column='icon', unique=True, upload_to=core.models.upload_directory_path, verbose_name='Icon')),
            ],
            options={
                'verbose_name': 'Invoice Icon',
                'verbose_name_plural': 'Invoice Icons',
                'db_table': 'InvoiceIcon',
            },
        ),
    ]