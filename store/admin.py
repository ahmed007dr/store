from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('Product_name', 'price', 'stock', 'created_date', 'updated_date', 'category')

admin.site.register(Product, ProductAdmin)