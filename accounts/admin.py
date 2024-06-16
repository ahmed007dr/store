from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login','is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Account, AccountAdmin)