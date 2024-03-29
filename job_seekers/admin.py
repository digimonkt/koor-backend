from django.contrib import admin
from .models import (
    EducationRecord, JobSeekerLanguageProficiency, EmploymentRecord,
    JobSeekerSkill, AppliedJob, AppliedJobAttachmentsItem,
    SavedJob, JobPreferences, Categories, Resume
)

admin.site.register(EducationRecord)
admin.site.register(JobSeekerLanguageProficiency)
admin.site.register(EmploymentRecord)
admin.site.register(JobSeekerSkill)
admin.site.register(AppliedJob)
admin.site.register(AppliedJobAttachmentsItem)
admin.site.register(SavedJob)
admin.site.register(JobPreferences)
admin.site.register(Categories)
admin.site.register(Resume)
