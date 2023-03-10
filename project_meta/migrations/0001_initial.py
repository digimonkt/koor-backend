# Generated by Django 4.1.5 on 2023-02-02 15:35

import core.models
from django.db import migrations, models
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Media",
            fields=[
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
                    "file_path",
                    models.FileField(
                        db_column="file_path",
                        unique=True,
                        upload_to=core.models.upload_directory_path,
                        verbose_name="File Path",
                    ),
                ),
                (
                    "media_type",
                    models.CharField(
                        choices=[
                            ("image", "Image"),
                            ("video", "Video"),
                            ("document", "Document"),
                        ],
                        db_column="media_type",
                        default="image",
                        max_length=250,
                        verbose_name="Media Type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Media",
                "verbose_name_plural": "Media",
                "db_table": "Media",
            },
        ),
    ]
