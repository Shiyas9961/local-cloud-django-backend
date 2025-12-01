"""Users app admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("username", "email", "is_staff", "is_active", "is_avatar_uploaded")
    readonly_fields = ("avatar_url",)