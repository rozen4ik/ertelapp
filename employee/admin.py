from django.contrib import admin
from employee.models import Profile, Department, Position


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "chat_id", "position_dep_id")
    list_display_links = ("id", "user", "chat_id", "position_dep_id")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "department_id")
    list_display_links = ("id", "name", "department_id")

