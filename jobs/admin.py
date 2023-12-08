from django.contrib import admin

from .models import (
    JobAttachmentsItem, JobCategory, 
    JobDetails, JobsLanguageProficiency,
    JobFilters, JobSubCategory,
    JobShare
    )

class JobDetailsAdmin(admin.ModelAdmin):
    list_display = ('title','display_job_category', 'deadline', 'status')
    
    
    def display_job_category(self, obj):
        return ", ".join([job_category.title for job_category in obj.job_category.all()])



admin.site.register(JobDetails, JobDetailsAdmin)

# admin.site.register(JobDetails)
admin.site.register(JobCategory)
admin.site.register(JobSubCategory)
admin.site.register(JobAttachmentsItem)
admin.site.register(JobsLanguageProficiency)
admin.site.register(JobFilters)
admin.site.register(JobShare)
