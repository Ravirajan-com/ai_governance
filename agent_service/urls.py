from django.urls import path

from .views import AgentDataAPIView


app_name = "agent_service"

urlpatterns = [
    path("data/", AgentDataAPIView.as_view(), name="agent-data"),
]

#