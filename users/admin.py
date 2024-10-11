from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ("username", "first_name", "last_name", "email")


admin.site.register(User, UserAdmin)
