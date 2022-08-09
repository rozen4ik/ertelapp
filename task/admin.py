from django.contrib import admin
from .models import *


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_task",
        "time_task",
        "text_task",
        "address_task",
        "author_task",
        "employee_task",
        "line_task",
        "status_task",
        "type_task",
        "business_trip",
        "note_task",
        "datetime_note_task"
    )
    list_display_links = (
        "id",
        "date_task",
        "time_task",
        "text_task",
        "address_task",
        "author_task",
        "employee_task",
        "line_task",
        "status_task",
        "type_task",
        "business_trip",
        "note_task",
        "datetime_note_task"
    )
