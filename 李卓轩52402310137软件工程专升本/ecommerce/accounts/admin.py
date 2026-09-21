from django.contrib import admin
from accounts.models import User, Address

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_active', 'created_at', 'last_login')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_active', 'created_at')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'province', 'city', 'district', 'is_default')
    search_fields = ('user__username', 'name', 'phone')

admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
