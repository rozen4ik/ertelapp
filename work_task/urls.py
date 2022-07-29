from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('work_task/', views.index_bot),
    path('work_task/delete/<int:id>/', views.delete_work_task),
    path('work_task/<int:id>/', views.show_work_task_for_task, name="work"),
]

urlpatterns = format_suffix_patterns(urlpatterns)