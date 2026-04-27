from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization, User
from .serializers import OrganizationSerializer, UserSerializer


class OrganizationListCreateAPIView(APIView):
    def get(self, request):
        serializer = OrganizationSerializer(Organization.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserListCreateAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(User.objects.select_related("organization").all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
