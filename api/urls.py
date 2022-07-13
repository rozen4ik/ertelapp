from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('api/drf-auth', include('rest_framework.urls')),
    path('api/tasks/', views.TaskList.as_view()),
    path('api/tasks/<int:pk>/', views.TaskDetail.as_view()),
    path('api/work_tasks/', views.WorkTaskList.as_view()),
    path('api/work_tasks/<int:pk>/', views.WorkTaskDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
