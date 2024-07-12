from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.contrib import admin 
from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login','is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    
    list_display_links = ('email','username')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'

    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Account, AccountAdmin)
