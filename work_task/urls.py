from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("work_tasks/", views.index_bot),
    path("work_tasks/<int:id>/", views.show_work_task_for_task, name="work"),
    path("export_excel_work_task", views.export_excel_work_task, name="export-excel-work-task"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
