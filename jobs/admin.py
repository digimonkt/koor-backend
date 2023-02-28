from django.contrib import admin

from .models import JobAttachmentsItem, JobCategory, JobDetails, JobsLanguageProficiency

admin.site.register(JobDetails)
admin.site.register(JobCategory)
admin.site.register(JobAttachmentsItem)
admin.site.register(JobsLanguageProficiency)
