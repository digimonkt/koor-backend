# Generated by Django 4.1.5 on 2023-02-02 17:35

from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("project_meta", "0002_tag"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
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
                    "title",
                    models.CharField(
                        db_column="title", max_length=255, verbose_name="Title"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, db_column="slug", null=True, unique=True
                    ),
                ),
                (
                    "currency_code",
                    models.CharField(
                        db_column="currency_code",
                        max_length=5,
                        verbose_name="Currency Code",
                    ),
                ),
                (
                    "country_code",
                    models.CharField(
                        db_column="country_code",
                        max_length=5,
                        verbose_name="Country Code",
                    ),
                ),
                (
                    "iso_code2",
                    models.CharField(
                        db_column="iso_code2", max_length=10, verbose_name="ISO Code 2"
                    ),
                ),
                (
                    "iso_code3",
                    models.CharField(
                        db_column="iso_code3", max_length=10, verbose_name="ISO Code 3"
                    ),
                ),
            ],
            options={
                "verbose_name": "Country",
                "verbose_name_plural": "Countries",
                "db_table": "Country",
            },
        ),
        migrations.CreateModel(
            name="EducationLevel",
            fields=[
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
                    "title",
                    models.CharField(
                        db_column="title", max_length=255, verbose_name="Title"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, db_column="slug", null=True, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Education Level",
                "verbose_name_plural": "Education Levels",
                "db_table": "EducationLevel",
            },
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
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
                    "title",
                    models.CharField(
                        db_column="title", max_length=255, verbose_name="Title"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, db_column="slug", null=True, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Language",
                "verbose_name_plural": "Langauges",
                "db_table": "Language",
            },
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
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
                    "title",
                    models.CharField(
                        db_column="title", max_length=255, verbose_name="Title"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, db_column="slug", null=True, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Skill",
                "verbose_name_plural": "Skills",
                "db_table": "Skill",
            },
        ),
        migrations.CreateModel(
            name="City",
            fields=[
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
                    "title",
                    models.CharField(
                        db_column="title", max_length=255, verbose_name="Title"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, db_column="slug", null=True, unique=True
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        db_column="country",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_country",
                        to="project_meta.country",
                        verbose_name="Country",
                    ),
                ),
            ],
            options={
                "verbose_name": "City",
                "verbose_name_plural": "Cities",
                "db_table": "City",
            },
        ),
    ]
