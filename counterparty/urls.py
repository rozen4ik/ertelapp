from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('counterparty_to/', views.counterparty_to),
    path('counterparty_warranty_obligations/', views.counterparty_warranty_obligations),
    path('counterparty_to/create/', views.create_counterparty_to),
    path('counterparty_warranty_obligations/create/', views.create_countrparty_warranty_obligations),
    path('counterparty_to/<int:id>/', views.counterparty_to_detail),
    path('counterparty_warranty_obligations/<int:id>/', views.countrparty_warranty_obligations_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
