from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Model as RegistryModel
from .models import OrganizationModelAccess, UserModelPermission
from .serializers import (
    ModelSerializer,
    OrganizationModelAccessSerializer,
    UserModelPermissionSerializer,
)


class ModelListCreateAPIView(APIView):
    def get(self, request):
        serializer = ModelSerializer(RegistryModel.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrganizationModelAccessListCreateAPIView(APIView):
    def get(self, request):
        serializer = OrganizationModelAccessSerializer(
            OrganizationModelAccess.objects.select_related("model").all(),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganizationModelAccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserModelPermissionListCreateAPIView(APIView):
    def get(self, request):
        serializer = UserModelPermissionSerializer(
            UserModelPermission.objects.select_related("model").all(),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserModelPermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
