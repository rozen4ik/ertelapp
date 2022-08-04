from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("api/drf-auth", include("rest_framework.urls")),
    path("api/tasks/<str:employee_task>/", views.api_task_list),
    path("api/tasks/<str:employee_task>/<int:pk>/", views.api_task_detail),
    path("api/work_tasks/", views.api_work_task_list),
    path("api/work_tasks/<int:pk>/", views.api_work_task_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns)
