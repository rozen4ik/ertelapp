from django.contrib import admin
from work_task.models import WorkTask


class WorkTaskAdmin(admin.ModelAdmin):
    list_display = (
        "date_work_task",
        "time_work_task",
        "employee_work_task",
        "address_work_task",
        "status_work_task",
        "task"
    )


admin.site.register(WorkTask, WorkTaskAdmin)
