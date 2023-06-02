from django.contrib import admin
from .models import VendorTag, VendorSector

# Register your models here.
admin.site.register(VendorTag)
admin.site.register(VendorSector)