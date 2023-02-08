# Generated by Django 4.1.5 on 2023-02-02 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project_meta", "0003_country_educationlevel_language_skill_city"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobSeekerProfile",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("is_removed", models.BooleanField(default=False)),
                (
                    "id",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "active",
                    models.BooleanField(
                        blank=True,
                        db_column="active",
                        default=True,
                        null=True,
                        verbose_name="Active",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")],
                        db_column="gender",
                        max_length=255,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "dob",
                    models.DateField(
                        blank=True,
                        db_column="dob",
                        null=True,
                        verbose_name="Date of Birth",
                    ),
                ),
                (
                    "employment_status",
                    models.CharField(
                        choices=[
                            ("employed", "Employed"),
                            ("other", "Other"),
                            ("fresher", "Fresher"),
                        ],
                        db_column="employment_status",
                        max_length=255,
                        verbose_name="Employment Status",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        db_column="description",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "market_information_notification",
                    models.BooleanField(
                        db_column="market_information_notification",
                        default=True,
                        verbose_name="Market Information Notification",
                    ),
                ),
                (
                    "job_notification",
                    models.BooleanField(
                        db_column="job_notification",
                        default=True,
                        verbose_name="Job Notification",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "highest_education",
                    models.ForeignKey(
                        blank=True,
                        db_column="highest_education",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_highest_educations",
                        to="project_meta.educationlevel",
                        verbose_name="Highest Education",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_modified_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified By",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        db_column="user",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Job Seeker Profile",
                "verbose_name_plural": "Job Seeker Profiles",
                "db_table": "JobSeekerProfile",
            },
        ),
    ]
