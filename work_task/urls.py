from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("work_tasks/", views.index_bot),
    path("work_tasks/<int:id>/", views.show_work_task_for_task, name="work"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
