from django.contrib import admin
from employee.models import Profile, Department, Position


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "chat_id", "position_dep_id")


# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")


class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "department_id")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department)
admin.site.register(Position, PositionAdmin)
