from django.contrib import admin
from .models import (
    TenderAttachmentsItem, TenderCategory, TenderDetails
)

admin.site.register(TenderAttachmentsItem)
admin.site.register(TenderCategory)
admin.site.register(TenderDetails)
