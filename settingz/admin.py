from django.contrib import admin
from .models import Settings


admin.site.register(Settings)



# @admin.register(Settings)
# class SettingsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'call_us', 'email_us', 'phone', 'address')
#     search_fields = ('name', 'call_us', 'emails_us', 'phone', 'address')
#     list_filter = ('name',)
#     ordering = ('name',)
    
#     # Optionally, you can customize the form layout if needed
#     fieldsets = (
#         (None, {
#             'fields': ('name', 'logo', 'subtitle', 'call_us', 'emails_us', 'emails', 'phone', 'address')
#         }),
#     )
#     readonly_fields = ('logo',)
