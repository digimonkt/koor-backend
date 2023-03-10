# Generated by Django 4.1.5 on 2023-02-02 15:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import users.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("project_meta", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
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
                    "email",
                    models.EmailField(
                        blank=True,
                        db_column="email",
                        max_length=254,
                        null=True,
                        verbose_name="Email Address",
                    ),
                ),
                (
                    "mobile_number",
                    models.CharField(
                        blank=True,
                        db_column="mobile_number",
                        max_length=13,
                        null=True,
                        verbose_name="Mobile Number",
                    ),
                ),
                (
                    "country_code",
                    models.CharField(
                        blank=True,
                        db_column="country_code",
                        max_length=250,
                        null=True,
                        verbose_name="Country Code",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        db_column="name",
                        max_length=250,
                        null=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "Admin"),
                            ("job_seeker", "Job Seeker"),
                            ("employer", "Employer"),
                            ("vendor", "Vendor"),
                        ],
                        db_column="role",
                        max_length=250,
                        verbose_name="Role",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        db_column="image",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_image",
                        to="project_meta.media",
                        verbose_name="Image",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "db_table": "User",
            },
            managers=[("objects", users.managers.UserManager()),],
        ),
    ]
