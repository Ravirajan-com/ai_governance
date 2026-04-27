from rest_framework import serializers

from .models import Feature, OrganizationFeatureAccess, UserFeaturePermission


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Feature name cannot be blank.")
        return value

    def validate_description(self, value: str) -> str:
        return value.strip()


class OrganizationFeatureAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationFeatureAccess
        fields = ["id", "organization_id", "feature", "is_active"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if self.instance is None and OrganizationFeatureAccess.objects.filter(
            organization_id=attrs["organization_id"],
            feature=attrs["feature"],
        ).exists():
            raise serializers.ValidationError(
                "Organization access for this feature already exists."
            )
        return attrs


class UserFeaturePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeaturePermission
        fields = ["id", "user_id", "feature", "can_read", "can_write", "can_delete"]
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

        if self.instance is None and UserFeaturePermission.objects.filter(
            user_id=attrs["user_id"],
            feature=attrs["feature"],
        ).exists():
            raise serializers.ValidationError(
                "User permissions for this feature already exist."
            )
        return attrs


class FeaturePermissionCheckSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    feature_id = serializers.UUIDField()
    organization_id = serializers.UUIDField(required=False)
