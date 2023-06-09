# Generated by Django 4.1.5 on 2023-06-09 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_meta', '0016_rename_sector_opportunitytype_and_more'),
        ('superadmin', '0020_alter_categorylogo_logo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorylogo',
            options={'ordering': ['-created'], 'verbose_name': 'Category Logo', 'verbose_name_plural': 'Category Logos'},
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('title', models.CharField(db_column='title', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, db_column='slug', null=True, unique=True)),
                ('client_name', models.CharField(db_column='client_name', max_length=255, verbose_name='Client Name')),
                ('client_company', models.CharField(db_column='client_company', max_length=255, verbose_name='Client Company')),
                ('client_position', models.CharField(db_column='client_position', max_length=255, verbose_name='Client Position')),
                ('description', models.TextField(blank=True, db_column='description', null=True, verbose_name='Description')),
                ('status', models.BooleanField(blank=True, db_column='status', default=False, null=True, verbose_name='Status')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('image', models.OneToOneField(blank=True, db_column='image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_image', to='project_meta.media', verbose_name='Image')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
                'db_table': 'Testimonial',
                'ordering': ['-created'],
            },
        ),
    ]