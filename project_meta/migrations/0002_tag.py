# Generated by Django 4.1.5 on 2023-02-02 16:41

from django.db import migrations, models
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("project_meta", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
                "db_table": "Tag",
            },
        ),
    ]
