from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include("task.urls")),
    path("", include("work_task.urls")),
    path("", include("counterparty.urls")),
    path("", include("api.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

