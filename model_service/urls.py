from django.urls import path

from .views import (
    ModelListCreateAPIView,
    OrganizationModelAccessListCreateAPIView,
    UserModelPermissionListCreateAPIView,
)


app_name = "model_service"

urlpatterns = [
    path("", ModelListCreateAPIView.as_view(), name="model-list-create"),
    path("organization-access/", OrganizationModelAccessListCreateAPIView.as_view(), name="organization-model-access-list-create"),
    path("user-permissions/", UserModelPermissionListCreateAPIView.as_view(), name="user-model-permission-list-create"),
]
