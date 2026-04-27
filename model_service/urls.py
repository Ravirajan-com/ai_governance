from django.urls import path

from .views import (
    FeatureListCreateAPIView,
    FeaturePermissionCheckAPIView,
    OrganizationFeatureAccessListCreateAPIView,
    UserFeaturePermissionListCreateAPIView,
)


app_name = "model_service"

urlpatterns = [
    path("features/", FeatureListCreateAPIView.as_view(), name="feature-list-create"),
    path(
        "features/permission-check/",
        FeaturePermissionCheckAPIView.as_view(),
        name="feature-permission-check",
    ),
    path(
        "organization-feature-access/",
        OrganizationFeatureAccessListCreateAPIView.as_view(),
        name="organization-feature-access-list-create",
    ),
    path(
        "user-feature-permissions/",
        UserFeaturePermissionListCreateAPIView.as_view(),
        name="user-feature-permission-list-create",
    ),
]
