from django.contrib.auth.admin import UserAdmin
from .models import Account
from django.contrib import admin

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login','is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    
    list_display_links = ('email','username')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)