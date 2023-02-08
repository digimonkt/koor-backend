from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .models import User


# Register your models here.
@admin.register(User)  # Register User model created by developer
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'mobile_number', 'country_code', 'role',)
        }),
        (_('Personal info'), {
            'fields': ('name', 'image')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',)
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile_number', 'role', 'country_code', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'mobile_number', 'is_active', 'role',)
    list_display_links = ('email', 'mobile_number',)
    ordering = ('date_joined',)
