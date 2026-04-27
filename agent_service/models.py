import uuid

from django.db import models
from django.utils import timezone


class AgentDataLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_name = models.CharField(max_length=255)
    payload = models.JSONField()
    received_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = "agent_data_logs"
        ordering = ["-received_at"]

    def __str__(self) -> str:
        return f"{self.agent_name} @ {self.received_at.isoformat()}"
