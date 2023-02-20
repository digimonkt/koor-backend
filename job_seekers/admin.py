from django.contrib import admin
from .models import (
    EducationRecord, JobSeekerLanguageProficiency, EmploymentRecord,
    JobSeekerSkill
)

admin.site.register(EducationRecord)
admin.site.register(JobSeekerLanguageProficiency)
admin.site.register(EmploymentRecord)
admin.site.register(JobSeekerSkill)
