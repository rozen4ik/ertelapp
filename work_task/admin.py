from django.contrib import admin
from work_task.models import WorkTask


@admin.register(WorkTask)
class WorkTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_work_task",
        "time_work_task",
        "employee_work_task",
        "address_work_task",
        "status_work_task",
        "task"
    )
    list_display_links = (
        "id",
        "date_work_task",
        "time_work_task",
        "employee_work_task",
        "address_work_task",
        "status_work_task",
        "task"
    )
