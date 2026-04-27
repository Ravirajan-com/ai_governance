from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("identity/", include("identity_service.urls")),
    path("models/", include("model_service.urls")),
    path("agent/", include("agent_service.urls")),
]
