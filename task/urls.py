from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('edit/<int:id>/', views.edit, name="edit"),
    # path('delete/<int:id>/', views.delete),
    path('export_excel', views.export_excel, name="export-excel"),
    path('export_excel_work_task', views.export_excel_work_task, name="export-excel-work-task"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
