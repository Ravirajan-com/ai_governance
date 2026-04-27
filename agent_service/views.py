from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AgentDataLogSerializer
from .services.agent_data import log_agent_data


class AgentDataAPIView(APIView):
    def post(self, request):
        serializer = AgentDataLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = log_agent_data(serializer.validated_data)
        return Response(
            {
                "success": True,
                "data": AgentDataLogSerializer(instance).data,
            },
            status=status.HTTP_201_CREATED,
        )
