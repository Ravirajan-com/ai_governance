import uuid

from django.db import models
from django.utils import timezone


class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = "model_registry"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class OrganizationModelAccess(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        related_name="organization_accesses",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "organization_model_accesses"
        unique_together = ("organization_id", "model")

    def __str__(self) -> str:
        return f"{self.organization_id} -> {self.model.name}"


class UserModelPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        related_name="user_permissions",
    )
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        db_table = "user_model_permissions"
        unique_together = ("user_id", "model")

    def __str__(self) -> str:
        return f"{self.user_id} permissions for {self.model.name}"
