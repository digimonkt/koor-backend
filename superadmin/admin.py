from django.contrib import admin
from project_meta.models import EducationLevel, Skill
from .models import SMTPSetting, Content, GooglePlaceApi

admin.site.register(EducationLevel)
admin.site.register(Skill)
admin.site.register(SMTPSetting)
admin.site.register(Content)
admin.site.register(GooglePlaceApi)
