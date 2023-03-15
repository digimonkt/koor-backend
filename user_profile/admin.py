from django.contrib import admin
from .models import JobSeekerProfile, EmployerProfile

# Register your models here.
admin.site.register(JobSeekerProfile)
admin.site.register(EmployerProfile)