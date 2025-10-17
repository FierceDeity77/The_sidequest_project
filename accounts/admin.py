from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ("email", "username", "created_at", "role")
    list_display = ("email", "username", "avatar", "created_at", "karma", "role", "is_staff", "is_active", "content_type")
    list_editable = ('username', 'role', 'content_type')


admin.site.register(CustomUser, CustomUserAdmin)