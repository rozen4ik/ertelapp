from django.contrib import admin
from history.models import HistoryStatusTask, HistoryNoteTask


@admin.register(HistoryStatusTask)
class HistoryStatusTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "datetime_history",
        "status_history",
        "employee_history",
        "task"
    )
    list_display_links = (
        "id",
        "datetime_history",
        "status_history",
        "employee_history",
        "task"
    )


@admin.register(HistoryNoteTask)
class HistoryNoteTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "datetime_history",
        "note_history",
        "employee_history",
        "task"
    )
    list_display_links = (
        "id",
        "datetime_history",
        "note_history",
        "employee_history",
        "task"
    )

