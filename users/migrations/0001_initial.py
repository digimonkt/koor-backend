# Generated by Django 4.1.5 on 2024-03-06 12:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import users.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('project_meta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('email', models.EmailField(blank=True, db_column='email', max_length=254, null=True, verbose_name='Email Address')),
                ('mobile_number', models.CharField(blank=True, db_column='mobile_number', max_length=13, null=True, verbose_name='Mobile Number')),
                ('country_code', models.CharField(blank=True, db_column='country_code', max_length=250, null=True, validators=[django.core.validators.RegexValidator(message='Invalid country code', regex='^\\+[1-9]\\d{0,2}$')], verbose_name='Country Code')),
                ('name', models.CharField(blank=True, db_column='name', max_length=250, null=True, verbose_name='Name')),
                ('social_login_id', models.CharField(blank=True, db_column='social_login_id', max_length=250, null=True, verbose_name='Social Login Id')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('job_seeker', 'Job Seeker'), ('employer', 'Employer'), ('vendor', 'Vendor')], db_column='role', max_length=250, verbose_name='Role')),
                ('source', models.CharField(choices=[('app', 'App'), ('apple', 'Apple'), ('facebook', 'Facebook'), ('google', 'Google')], db_column='source', default='app', max_length=250, verbose_name='Source')),
                ('otp', models.CharField(blank=True, db_column='otp', max_length=250, null=True, verbose_name='OTP')),
                ('verification_token', models.CharField(blank=True, db_column='verification_token', max_length=250, null=True, verbose_name='Verification Token')),
                ('otp_created_at', models.DateTimeField(blank=True, db_column='otp_created_at', null=True, verbose_name='OTP Created At')),
                ('is_verified', models.BooleanField(blank=True, db_column='is_verified', default=False, null=True, verbose_name='Is Verified')),
                ('is_online', models.BooleanField(blank=True, db_column='is_online', default=False, null=True, verbose_name='Is Online')),
                ('get_email', models.BooleanField(db_column='get_email', default=True, verbose_name='Get Email')),
                ('get_notification', models.BooleanField(db_column='get_notification', default=True, verbose_name='Get Notification')),
                ('is_company', models.BooleanField(db_column='is_company', default=False, verbose_name='Is Company')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('image', models.OneToOneField(blank=True, db_column='image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_image', to='project_meta.media', verbose_name='Image')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'User',
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='VisitorLog',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ip_address', models.GenericIPAddressField(blank=True, db_column='ip_address', null=True, verbose_name='IP Address')),
                ('agent', models.JSONField(blank=True, db_column='agent', null=True, verbose_name='Agent')),
                ('created_at', models.DateField(blank=True, db_column='created_at', null=True, verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Visitor Log',
                'verbose_name_plural': 'Visitor Logs',
                'db_table': 'VisitorLog',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(blank=True, db_column='active', default=True, null=True, verbose_name='Active')),
                ('ip_address', models.GenericIPAddressField(blank=True, db_column='ip_address', null=True, verbose_name='IP Address')),
                ('agent', models.JSONField(db_column='agent', null=True, verbose_name='Agent')),
                ('expire_at', models.DateTimeField(blank=True, db_column='expire_at', null=True, verbose_name='Expire At')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_user', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Session',
                'verbose_name_plural': 'User Sessions',
                'db_table': 'UserSession',
                'ordering': ['created'],
            },
        ),
    ]
