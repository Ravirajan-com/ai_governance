import uuid

from django.db import models
from django.utils import timezone


class Feature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = "feature_registry"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class OrganizationFeatureAccess(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        related_name="organization_accesses",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "organization_feature_accesses"
        unique_together = ("organization_id", "feature")

    def __str__(self) -> str:
        return f"{self.organization_id} -> {self.feature.name}"


class UserFeaturePermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        related_name="user_permissions",
    )
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        db_table = "user_feature_permissions"
        unique_together = ("user_id", "feature")

    def __str__(self) -> str:
        return f"{self.user_id} permissions for {self.feature.name}"
