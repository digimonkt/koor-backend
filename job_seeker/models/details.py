from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from project_meta.models import (
    Media, Language, Skill)
from users.models import User


class EducationRecord(BaseModel, SoftDeleteModel, models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)sUser'
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        db_column="title",
    )
    start_date = models.DateField(
        verbose_name=_('Start Date'),
        db_column='start_date'
    )
    end_date = models.DateField(
        verbose_name=_('End Date'),
        blank=True,
        null=True,
        db_column='end_date'
    )
    institute = models.CharField(
        verbose_name=_('Institute'),
        max_length=255,
        db_column="institute",
    )
    organization = models.CharField(
        verbose_name=_('Organization'),
        max_length=255,
        db_column="organization",
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
        db_column="description",
    )

    def __str__(self):
        return str(self.title) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Education Record"
        verbose_name_plural = "Education Records"
        db_table = "EducationRecord"


class EmploymentRecord(BaseModel, SoftDeleteModel, models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)sUser'
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        db_column="title",
    )
    start_date = models.DateField(
        verbose_name=_('Start Date'),
        db_column='start_date'
    )
    end_date = models.DateField(
        verbose_name=_('End Date'),
        blank=True,
        null=True,
        db_column='end_date'
    )
    present = models.BooleanField(
        verbose_name=_('Present'),
        null=True,
        blank=True,
        default=True,
        db_column="present",
    )
    organization = models.CharField(
        verbose_name=_('Organization'),
        max_length=255,
        db_column="organization",
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
        db_column="description",
    )

    def __str__(self):
        return str(self.title) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Employment Record"
        verbose_name_plural = "Employment Records"
        db_table = "EmploymentRecord"


class Resume(BaseModel, SoftDeleteModel, models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)sUser'
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        db_column="title",
    )
    file_path = models.ForeignKey(
        Media,
        verbose_name=_('File Path'),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)sFilePath'
    )

    def __str__(self):
        return str(self.title) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"
        db_table = "Resume"


class JobSeekerLanguageProficiency(BaseModel, SoftDeleteModel, models.Model):
    FLUENCY_CHOICE = (
        ('basic', "Basic"),
        ('conversational', "Conversational"),
        ('fluent', "Fluent"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)sUser'
    )
    language = models.ForeignKey(
        Language,
        verbose_name=_('Language'),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)sLanguage'
    )
    written = models.CharField(
        verbose_name=_('Written'),
        max_length=255,
        db_column="written",
        choices=FLUENCY_CHOICE,
    )
    spoken = models.CharField(
        verbose_name=_('Spoken'),
        max_length=255,
        db_column="spoken",
        choices=FLUENCY_CHOICE,
    )

    def __str__(self):
        return str(self.language) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Job Seeker Language Proficiency"
        verbose_name_plural = "Job Seeker Language Proficiencies"
        db_table = "JobSeekerLanguageProficiency"


class JobSeekerSkill(BaseModel, SoftDeleteModel, models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)sUser'
    )
    skill = models.ForeignKey(
        Skill,
        verbose_name=_('Skill'),
        on_delete=models.CASCADE,
        db_column="skill",
        related_name='%(app_label)s_%(class)sSkill'
    )

    def __str__(self):
        return str(self.skill) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Job Seeker Skill"
        verbose_name_plural = "Job Seeker Skills"
        db_table = "JobSeekerSkill"
