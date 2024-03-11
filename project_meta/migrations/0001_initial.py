# Generated by Django 4.1.5 on 2024-03-06 12:59

import core.models
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_column='title', max_length=150, verbose_name='Title')),
                ('iso3', models.CharField(db_column='iso3', max_length=10, verbose_name='ISO Code 3')),
                ('iso2', models.CharField(db_column='iso2', max_length=10, verbose_name='ISO Code 2')),
                ('phone_code', models.CharField(db_column='phone_code', max_length=50, verbose_name='Phone Code')),
                ('currency', models.CharField(db_column='currency', max_length=20, verbose_name='Currency')),
            ],
            options={
                'verbose_name': 'All Country',
                'verbose_name_plural': 'All Countries',
                'db_table': 'AllCountry',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('title', models.CharField(db_column='title', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, db_column='slug', max_length=455, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Choice',
                'verbose_name_plural': 'Choices',
                'db_table': 'Choice',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('title', models.CharField(db_column='title', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, db_column='slug', max_length=455, null=True, unique=True)),
                ('currency_code', models.CharField(db_column='currency_code', max_length=5, verbose_name='Currency Code')),
                ('country_code', models.CharField(db_column='country_code', max_length=5, verbose_name='Country Code')),
                ('iso_code2', models.CharField(db_column='iso_code2', max_length=10, verbose_name='ISO Code 2')),
                ('iso_code3', models.CharField(db_column='iso_code3', max_length=10, verbose_name='ISO Code 3')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'db_table': 'Country',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='EducationLevel',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('title', models.CharField(db_column='title', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, db_column='slug', max_length=455, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Education Level',
                'verbose_name_plural': 'Education Levels',
                'db_table': 'EducationLevel',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('title', models.CharField(db_column='title', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, db_column='slug', max_length=455, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Langauges',
                'db_table': 'Language',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, db_column='title', max_length=250, null=True, verbose_name='Title')),
                ('file_path', models.FileField(db_column='file_path', upload_to=core.models.upload_directory_path, verbose_name='File Path')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('document', 'Document')], db_column='media_type', default='image', max_length=250, verbose_name='Media Type')),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Media',
                'db_table': 'Media',
            },
        ),
        migrations.CreateModel(
            name='OpportunityType',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('title', models.CharField(db_column='title', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, db_column='slug', max_length=455, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Opportunity Type',
                'verbose_name_plural': 'Opportunity Types',
                'db_table': 'OpportunityType',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('title', models.CharField(db_column='title', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, db_column='slug', max_length=455, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
                'db_table': 'Skill',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('title', models.CharField(db_column='title', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, db_column='slug', max_length=455, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'db_table': 'Tag',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('title', models.CharField(db_column='title', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, db_column='slug', max_length=455, null=True, unique=True)),
                ('country', models.ForeignKey(db_column='country', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_country', to='project_meta.country', verbose_name='Country')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
                'db_table': 'City',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='AllCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_column='title', max_length=150, verbose_name='Title')),
                ('country', models.ForeignKey(db_column='country', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_country', to='project_meta.allcountry', verbose_name='Country')),
            ],
            options={
                'verbose_name': 'All City',
                'verbose_name_plural': 'All Cities',
                'db_table': 'AllCity',
                'ordering': ['title'],
            },
        ),
    ]
