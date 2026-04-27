from django.urls import path

from .views import OrganizationListCreateAPIView, UserListCreateAPIView


app_name = "identity_service"

urlpatterns = [
    path("organizations/", OrganizationListCreateAPIView.as_view(), name="organization-list-create"),
    path("users/", UserListCreateAPIView.as_view(), name="user-list-create"),
]
