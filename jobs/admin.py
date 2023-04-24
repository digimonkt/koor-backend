from django.contrib import admin

from .models import (
    JobAttachmentsItem, JobCategory, 
    JobDetails, JobsLanguageProficiency,
    JobFilters, JobSubCategory,
    JobShare
    )

admin.site.register(JobDetails)
admin.site.register(JobCategory)
admin.site.register(JobSubCategory)
admin.site.register(JobAttachmentsItem)
admin.site.register(JobsLanguageProficiency)
admin.site.register(JobFilters)
admin.site.register(JobShare)
