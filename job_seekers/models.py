from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)

from users.models import User, TimeStampedModel

from jobs.models import JobDetails, JobSubCategory

from project_meta.models import (
    Media, Language, Skill,
    EducationLevel
)


class EducationRecord(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This Django model class represents the education record details for a jobseeker. The fields are as follows:

    - `user`: The user who this education record belongs to.
    - `title`: The title of the education record.
    - `start_date`: The start date of the education record.
    - `end_date`: The end date of the education record.
    - `institute`: The institute associated with the education record.
    - `education_level`: The education level which is education record belongs to.
    """
    user = models.ForeignKey(
        to=User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
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
    education_level = models.ForeignKey(
        to=EducationLevel,
        verbose_name=_('Education Level'),
        on_delete=models.CASCADE,
        db_column="education_level",
        related_name='%(app_label)s_%(class)s_education'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Education Record"
        verbose_name_plural = "Education Records"
        db_table = "EducationRecord"
        ordering = ['-created']


class EmploymentRecord(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This Django model class represents the employment record details for a job seeker.

    Columns
    - `user`: The user who this employment record belongs to.
    - `title`: The title of the employment record.
    - `start_date`: The start date of the employment record.
    - `end_date`: The end date of the employment record.
    - `organization`: The organization associated with the employment record.
    - `description`: A description of the employment record.
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
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
        return str(self.title)

    class Meta:
        verbose_name = "Employment Record"
        verbose_name_plural = "Employment Records"
        db_table = "EmploymentRecord"
        ordering = ['-created']


class Resume(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This Django model class represents the resume for a job seeker. The fields are as follows:

    - `user`: The user who this resume belongs to.
    - `title`: The title of the resume.
    - `file_path`: The file containing the resume.
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        db_column="title",
    )
    file_path = models.OneToOneField(
        Media,
        verbose_name=_('File Path'),
        on_delete=models.CASCADE,
        db_column="file_path",
        related_name='%(app_label)s_%(class)s_file_path'
    )

    def __str__(self):
        return str(self.title) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"
        db_table = "Resume"
        ordering = ['-created']


class JobSeekerLanguageProficiency(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This Django model class represents the language proficiency of a job seeker. The fields are as follows:

    - `user`: The user who this language proficiency belongs to.
    - `language`: The language of the language proficiency.
    - `written`: The written proficiency level of the language.
    - `spoken`: The spoken proficiency level of the language.
    """
    FLUENCY_CHOICE = (
        ('basic', "Basic"),
        ('conversational', "Conversational"),
        ('fluent', "Fluent"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    language = models.ForeignKey(
        Language,
        verbose_name=_('Language'),
        on_delete=models.CASCADE,
        db_column="language",
        related_name='%(app_label)s_%(class)s_language'
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
        ordering = ['-created']


class JobSeekerSkill(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This Django model class represents the skill of a job seeker. The fields are as follows:

    - `user`: The user who this skill belongs to.
    - `skill`: The skill of the job seeker.
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    skill = models.ForeignKey(
        to=Skill,
        verbose_name=_('Skill'),
        on_delete=models.CASCADE,
        db_column="skill",
        related_name='%(app_label)s_%(class)s_skill'
    )

    def __str__(self):
        return str(self.skill) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Job Seeker Skill"
        verbose_name_plural = "Job Seeker Skills"
        db_table = "JobSeekerSkill"
        ordering = ['-created']


class SavedJob(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This is a Django model for a Saved Job object, associated with a JobSeeker user, with the following fields:

    - `user`: the user associated with the saved job
    - `job`: the job associated with the saved job
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    job = models.ForeignKey(
        JobDetails,
        verbose_name=_('Job'),
        on_delete=models.CASCADE,
        db_column="job",
        related_name='%(app_label)s_%(class)s_job'
    )
    notified = models.BooleanField(
        verbose_name=_('Notified'),
        null=True,
        blank=True,
        db_column="notified",
        default=False
    )

    def __str__(self):
        return str(self.job) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Saved Job"
        verbose_name_plural = "Saved Jobs"
        db_table = "SavedJob"
        ordering = ['-created']


class AppliedJob(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This is a Django model for an Applied Job object, associated with a JobSeeker user, with the following fields:

    - `user`: the user associated with the applied job
    - `job`: the job associated with the applied job
    - `shortlisted_at`: the date and time when the job was shortlisted
    - `rejected_at`: the date and time when the job was rejected
    - `resume`: the resume submitted for the job
    - `cover_letter`: the cover letter submitted for the job
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    job = models.ForeignKey(
        JobDetails,
        verbose_name=_('Job'),
        on_delete=models.CASCADE,
        db_column="job",
        related_name='%(app_label)s_%(class)s_job'
    )
    interview_at = models.DateTimeField(
        verbose_name=_('Interview Planned At'),
        null=True,
        blank=True,
        db_column="interview_at"
    )
    shortlisted_at = models.DateTimeField(
        verbose_name=_('Short Listed At'),
        null=True,
        blank=True,
        db_column="shortlisted_at"
    )
    rejected_at = models.DateTimeField(
        verbose_name=_('Rejected At'),
        null=True,
        blank=True,
        db_column="rejected_at"
    )
    resume = models.ForeignKey(
        Media,
        verbose_name=_('Resume'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="resume",
        related_name='%(app_label)s_%(class)s_resume'
    )
    short_letter = models.TextField(
        verbose_name=_('Short Letter'),
        null=True,
        blank=True,
        db_column="short_letter",
    )

    def __str__(self):
        return str(self.job) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Applied Job"
        verbose_name_plural = "Applied Jobs"
        db_table = "AppliedJob"
        ordering = ['-created']


class AppliedJobAttachmentsItem(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This is a Django model for an Applied Job Attachment object, associated with an Applied Job item, with the following fields:

    - `applied_job`: the applied job associated with the attachment
    - `attachment`: the attachments uploaded for the applied job
    """
    applied_job = models.ForeignKey(
        AppliedJob,
        verbose_name=_('Applied Job'),
        on_delete=models.CASCADE,
        db_column="applied_job",
        null=True,
        related_name='%(app_label)s_%(class)s_applied_job'
    )
    attachment = models.OneToOneField(
        Media,
        verbose_name=_('Attachment'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="attachment",
        related_name='%(app_label)s_%(class)s_attachment'
    )

    def __str__(self):
        return str(self.applied_job)

    class Meta:
        verbose_name = "Applied Job Attachment Item"
        verbose_name_plural = "Applied Job Attachment Items"
        db_table = "AppliedJobAttachmentsItem"
        ordering = ['-created']


class JobPreferences(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    `JobPreferences` model stores the job Preferences of a user.

    Fields:
        - `user`: A foreign key to the User model.
        - `is_available`: A boolean indicating if the user is available for work.
        - `display_in_search`: A boolean indicating if the user's job Preferences are visible to employers.
        - `is_part_time`: A boolean indicating if the user is looking for part-time work.
        - `is_full_time`: A boolean indicating if the user is looking for full-time work.
        - `has_contract`: A boolean indicating if the user is looking for work with a contract.
        - `expected_salary`: A decimal field indicating the expected salary of the user.

    Meta:
        - `verbose_name`: A human-readable name for the model in singular form.
        - `verbose_name_plural`: A human-readable name for the model in plural form.
        - `db_table`: The name of the database table to use for the model.
        - `ordering`: The default ordering for the model.

    Inherits from:
        - `BaseModel`: A base model class with common fields and methods.
        - `SoftDeleteModel`: A model class that implements soft deletion.
        - `TimeStampedModel`: A model class that adds created and modified timestamps.
        - `models.Model`: The base class for all Django models.
    """

    user = models.OneToOneField(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    is_available = models.BooleanField(
        verbose_name=_('Is Available'),
        null=True,
        blank=True,
        db_column="is_available",
        default=False
    )
    display_in_search = models.BooleanField(
        verbose_name=_('Display in Search'),
        null=True,
        blank=True,
        db_column="display_in_search",
        default=False
    )
    is_part_time = models.BooleanField(
        verbose_name=_('Is Part Time'),
        null=True,
        blank=True,
        db_column="is_part_time",
        default=False
    )
    is_full_time = models.BooleanField(
        verbose_name=_('Is Full Time'),
        null=True,
        blank=True,
        db_column="is_full_time",
        default=False
    )
    has_contract = models.BooleanField(
        verbose_name=_('Has Contract'),
        null=True,
        blank=True,
        db_column="has_contract",
        default=False
    )
    expected_salary = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Expected Salary'),
        db_column="expected_salary",
    )

    class Meta:
        verbose_name = "Job Preferences"
        verbose_name_plural = "Job Preferences"
        db_table = "JobPreferences"
        ordering = ['-created']


class Categories(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
        Represents a category associated with a user in the job seeker application.

        Attributes:
            - `user (ForeignKey)`: The user associated with the category.
            - `category (ForeignKey)`: The job seeker category.

        Methods:
            - `__str__`: Returns a string representation of the category.

        Meta:
            - `verbose_name (str)`: A human-readable name for the model.
            - `verbose_name_plural (str)`: A human-readable plural name for the model.
            - `db_table (str)`: The name of the database table to use for the model.
            - `ordering (list)`: The default ordering for the model records.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    category = models.ForeignKey(
        JobSubCategory,
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
        db_column="category",
        related_name='%(app_label)s_%(class)s_categories'
    )

    def __str__(self):
        return str(self.category) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "Categories"
        ordering = ['-created']
