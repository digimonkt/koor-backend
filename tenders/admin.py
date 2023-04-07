from django.contrib import admin
from .models import (
    TenderAttachmentsItem, TenderCategory, TenderDetails,
    TenderFilter
)

admin.site.register(TenderAttachmentsItem)
admin.site.register(TenderCategory)
admin.site.register(TenderDetails)
admin.site.register(TenderFilter)
