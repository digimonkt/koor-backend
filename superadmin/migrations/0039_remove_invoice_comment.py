# Generated by Django 4.1.5 on 2023-08-11 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0038_invoice_points_alter_invoice_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='comment',
        ),
    ]