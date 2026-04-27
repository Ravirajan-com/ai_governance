from rest_framework import serializers

from .models import Model, OrganizationModelAccess, UserModelPermission


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Model name cannot be blank.")
        return value

    def validate_description(self, value: str) -> str:
        return value.strip()


class OrganizationModelAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationModelAccess
        fields = ["id", "organization_id", "model", "is_active"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if self.instance is None and OrganizationModelAccess.objects.filter(
            organization_id=attrs["organization_id"],
            model=attrs["model"],
        ).exists():
            raise serializers.ValidationError(
                "Organization access for this model already exists."
            )
        return attrs


class UserModelPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModelPermission
        fields = ["id", "user_id", "model", "can_read", "can_write", "can_delete"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        has_permission = any(
            attrs.get(permission, False)
            for permission in ("can_read", "can_write", "can_delete")
        )
        if not has_permission:
            raise serializers.ValidationError(
                "At least one permission must be enabled."
            )

        if self.instance is None and UserModelPermission.objects.filter(
            user_id=attrs["user_id"],
            model=attrs["model"],
        ).exists():
            raise serializers.ValidationError(
                "User permissions for this model already exist."
            )
        return attrs
