from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("counterparty/", views.list_counterparty),
    path("counterparty/create/", views.create_counterparty),
    path("counterparty/edit/<int:id>/", views.edit_counterparty),
    path("counterparty_to/", views.counterparty_to, name="edit_counterparty"),
    path("counterparty_warranty_obligations/", views.counterparty_warranty_obligations),
    path("counterparty_to/create/", views.create_counterparty_to),
    path("counterparty_warranty_obligations/create/", views.create_counterparty_warranty_obligations),
    path("counterparty_to/edit/<int:id>/", views.edit_counterparty_to, name="edit_to"),
    path("counterparty_warranty_obligations/edit/<int:id>/", views.edit_counterparty_warranty_obligations, name="edit_wo"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
