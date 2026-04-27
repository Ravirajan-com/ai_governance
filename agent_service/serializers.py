from rest_framework import serializers

from .models import AgentDataLog


class AgentDataLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentDataLog
        fields = ["id", "agent_name", "payload", "received_at"]
        read_only_fields = ["id", "received_at"]

    def validate_agent_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Agent name cannot be blank.")
        return value

    def validate_payload(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Payload must be a JSON object.")
        return value
