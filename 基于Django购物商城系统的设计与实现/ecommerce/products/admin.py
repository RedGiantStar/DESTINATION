from django.contrib import admin
from products.models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_active', 'created_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
