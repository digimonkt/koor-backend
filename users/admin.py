from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .models import User

# Register your models here.
@admin.register(User) # Register User model created by developer
#  Function for Display Model into superuser page
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'mobile', 'profile_role', )}),
        # (_('Personal info'), {'fields': ('full_name','phone_number', 'address',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile', 'profile_role', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'mobile', 'is_active','profile_role', )
    list_display_links = ('email', 'mobile',  )
    ordering = ('date_joined',)