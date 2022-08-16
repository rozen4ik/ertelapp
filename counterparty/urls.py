from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("counterparty/", views.list_counterparty),
    path("counterparty/create/", views.create_counterparty),
    path("counterparty/edit/<int:id>/", views.edit_counterparty),
]

urlpatterns = format_suffix_patterns(urlpatterns)
