from django.contrib import admin
from .models import (
    JobSeekerProfile, EmployerProfile, UserFilters
)

# Register your models here.
admin.site.register(JobSeekerProfile)
admin.site.register(EmployerProfile)
admin.site.register(UserFilters)