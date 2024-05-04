from django.contrib import admin
from project_meta.models import (
    EducationLevel, Skill,
    AllCountry, AllCity, Media
)
from .models import (
    SMTPSetting, Content, GooglePlaceApi,
    ResourcesContent, SocialUrl, AboutUs,
    FaqCategory, PointDetection, RechargeHistory,
    UserRights, UserSubRights, Rights,
    GoogleAddSenseCode, Invoice, InvoiceIcon,
    InvoiceFooter
)

admin.site.register(EducationLevel)
admin.site.register(Skill)
admin.site.register(SMTPSetting)
admin.site.register(Content)
admin.site.register(GooglePlaceApi)
admin.site.register(AllCountry)
admin.site.register(InvoiceIcon)
admin.site.register(InvoiceFooter)

class AllCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

admin.site.register(AllCity, AllCityAdmin)

# admin.site.register(AllCity)
admin.site.register(Media)
admin.site.register(ResourcesContent)
admin.site.register(SocialUrl)
admin.site.register(AboutUs)
admin.site.register(FaqCategory)
admin.site.register(PointDetection)
admin.site.register(RechargeHistory)
admin.site.register(GoogleAddSenseCode)
admin.site.register(UserRights)
admin.site.register(UserSubRights)
admin.site.register(Rights)
admin.site.register(Invoice)
