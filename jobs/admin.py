from django.contrib import admin

from .models import (
    JobAttachmentsItem, JobCategory, 
    JobDetails, JobsLanguageProficiency,
    JobFilters, JobSubCategory,
    JobShare
    )

class JobDetailsAdmin(admin.ModelAdmin):
    list_display = ('title','user', 'company', 'status')

admin.site.register(JobDetails, JobDetailsAdmin)

class JobSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title','category')

admin.site.register(JobSubCategory, JobSubCategoryAdmin)

# admin.site.register(JobDetails)
admin.site.register(JobCategory)
# admin.site.register(JobSubCategory)
admin.site.register(JobAttachmentsItem)
admin.site.register(JobsLanguageProficiency)
admin.site.register(JobFilters)
admin.site.register(JobShare)
