from django.contrib import admin
from .models import *


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "date_task",
        "time_task",
        "text_task",
        "address_task",
        "author_task",
        "employee_task",
        "line_task",
        "status_task",
        "business_trip"
    )


admin.site.register(Task, TaskAdmin)
