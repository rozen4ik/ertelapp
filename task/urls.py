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
    path('export_excel', views.export_excel, name="export-excel"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
