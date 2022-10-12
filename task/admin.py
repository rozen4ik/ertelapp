from django.contrib import admin
from .models import *


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_task",
        "time_task",
        "text_task",
        "object_task",
        "address_obj_task",
        "author_task",
        "employee_task",
        "urgency_task",
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
        "object_task",
        "address_obj_task",
        "author_task",
        "employee_task",
        "urgency_task",
        "line_task",
        "status_task",
        "type_task",
        "business_trip",
        "note_task",
        "datetime_note_task"
    )


@admin.register(TypeWork)
class TypeWorkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name"
    )

    list_display_links = (
        "id",
        "name"
    )
