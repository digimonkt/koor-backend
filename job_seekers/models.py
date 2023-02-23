from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from users.models import User, TimeStampedModel
from jobs.models import JobDetails
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
