from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('edit/<int:id>/', views.edit, name="edit"),
    # path('delete/<int:id>/', views.delete),
    path('work_task/', views.index_bot),
    path('work_task/delete/<int:id>/', views.delete_work_task),
    path('work_task/<int:id>/', views.show_work_task_for_task, name="work"),
    path('export_excel', views.export_excel, name="export-excel"),
    path('export_excel_work_task', views.export_excel_work_task, name="export-excel-work-task"),
    path('counterparty_to/', views.counterparty_to),
    path('countrparty_warranty_obligations/', views.countrparty_warranty_obligations),
    path('counterparty_to/create/', views.create_counterparty_to),
    path('countrparty_warranty_obligations/create/', views.create_countrparty_warranty_obligations),
    # path('counterparty_to/<int:id>/', views.counterparty_to_detail),
    # path('countrparty_warranty_obligations/<int:id>/', views.countrparty_warranty_obligations_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
