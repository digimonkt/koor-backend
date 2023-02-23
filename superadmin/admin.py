from django.contrib import admin
from project_meta.models import EducationLevel, Skill
from .models import SMTPSetting

admin.site.register(EducationLevel)
admin.site.register(Skill)
admin.site.register(SMTPSetting)
