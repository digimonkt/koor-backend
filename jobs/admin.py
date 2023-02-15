from django.contrib import admin

from .models import JobAttachmentsItem, JobCategory, JobDetails

admin.site.register(JobDetails)
admin.site.register(JobCategory)
admin.site.register(JobAttachmentsItem)
