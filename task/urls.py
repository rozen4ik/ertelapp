from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:id>/', views.index_detail, name="id_task"),
    path('create/', views.create),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),
    path('work_task/', views.index_bot),
    path('work_task/delete/<int:id>/', views.delete_work_task),
    path('export_excel', views.export_excel, name="export-excel"),
    path('export_excel_work_task', views.export_excel_work_task, name="export-excel-work-task"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
