from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("history_note_tasks/<int:id>/", views.history_note_task_detail, name="history_note_detail"),
    path("history_status_tasks/<int:id>/", views.history_status_task_detail, name="history_status_detail")
]

urlpatterns = format_suffix_patterns(urlpatterns)
