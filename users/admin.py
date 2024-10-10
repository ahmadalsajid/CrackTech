from django.contrib import admin
from .models import User, Student


class UserAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ("username", "first_name", "last_name", "email")


class StudentAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ("registration", "user")
    search_fields = (
        "registration",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
