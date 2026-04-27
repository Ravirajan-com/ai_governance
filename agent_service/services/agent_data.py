from agent_service.models import AgentDataLog


def log_agent_data(validated_data: dict) -> AgentDataLog:
    return AgentDataLog.objects.create(**validated_data)
