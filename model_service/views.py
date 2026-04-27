from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Feature, OrganizationFeatureAccess, UserFeaturePermission
from .serializers import (
    FeaturePermissionCheckSerializer,
    FeatureSerializer,
    OrganizationFeatureAccessSerializer,
    UserFeaturePermissionSerializer,
)


class FeatureListCreateAPIView(APIView):
    def get(self, request):
        serializer = FeatureSerializer(Feature.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FeatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrganizationFeatureAccessListCreateAPIView(APIView):
    def get(self, request):
        serializer = OrganizationFeatureAccessSerializer(
            OrganizationFeatureAccess.objects.select_related("feature").all(),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganizationFeatureAccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserFeaturePermissionListCreateAPIView(APIView):
    def get(self, request):
        serializer = UserFeaturePermissionSerializer(
            UserFeaturePermission.objects.select_related("feature").all(),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserFeaturePermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FeaturePermissionCheckAPIView(APIView):
    def get(self, request):
        serializer = FeaturePermissionCheckSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        feature_id = serializer.validated_data["feature_id"]
        organization_id = serializer.validated_data.get("organization_id")

        denied_response = {
            "allowed": False,
            "can_read": False,
            "can_write": False,
            "can_delete": False,
        }

        if not organization_id:
            return Response(denied_response, status=status.HTTP_200_OK)

        organization_access = OrganizationFeatureAccess.objects.filter(
            organization_id=organization_id,
            feature_id=feature_id,
            is_active=True,
        ).first()
        if organization_access is None:
            return Response(denied_response, status=status.HTTP_200_OK)

        user_permission = UserFeaturePermission.objects.filter(
            user_id=user_id,
            feature_id=feature_id,
        ).first()
        if user_permission is None:
            return Response(denied_response, status=status.HTTP_200_OK)

        response_data = {
            "allowed": any(
                [
                    user_permission.can_read,
                    user_permission.can_write,
                    user_permission.can_delete,
                ]
            ),
            "can_read": user_permission.can_read,
            "can_write": user_permission.can_write,
            "can_delete": user_permission.can_delete,
        }
        return Response(response_data, status=status.HTTP_200_OK)
