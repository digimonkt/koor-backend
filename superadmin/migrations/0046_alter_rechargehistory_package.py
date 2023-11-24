# Generated by Django 4.1.5 on 2023-11-22 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0045_rechargehistory_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rechargehistory',
            name='package',
            field=models.CharField(blank=True, choices=[('none', 'None'), ('gold', 'Gold'), ('silver', 'Silver'), ('copper', 'Copper')], db_column='package', default='none', max_length=250, null=True, verbose_name='Package'),
        ),
    ]
