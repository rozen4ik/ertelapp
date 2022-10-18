from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", views.index),
    path("create/", views.create),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("reports/", views.reports),
    path("export_excel", views.export_employee, name="export-employee"),
    path("export_counterparty", views.export_counterparty, name="export-counterparty")
]

urlpatterns = format_suffix_patterns(urlpatterns)
