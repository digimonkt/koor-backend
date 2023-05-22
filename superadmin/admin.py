from django.contrib import admin
from project_meta.models import (
    EducationLevel, Skill,
    AllCountry, AllCity, Media
)
from .models import (
    SMTPSetting, Content, GooglePlaceApi,
    ResourcesContent, SocialUrl
)

admin.site.register(EducationLevel)
admin.site.register(Skill)
admin.site.register(SMTPSetting)
admin.site.register(Content)
admin.site.register(GooglePlaceApi)
admin.site.register(AllCountry)
admin.site.register(AllCity)
admin.site.register(Media)
admin.site.register(ResourcesContent)
admin.site.register(SocialUrl)
