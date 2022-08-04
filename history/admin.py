from django.contrib import admin
from history.models import HistoryStatusTask, HistoryNoteTask


class HistoryStatusTaskAdmin(admin.ModelAdmin):
    list_display = (
        "datetime_history",
        "status_history",
        "employee_history",
        "task"
    )


class HistoryNoteTaskAdmin(admin.ModelAdmin):
    list_display = (
        "datetime_history",
        "note_history",
        "employee_history",
        "task"
    )


admin.site.register(HistoryStatusTask, HistoryStatusTaskAdmin)
admin.site.register(HistoryNoteTask, HistoryNoteTaskAdmin)
