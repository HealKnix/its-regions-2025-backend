from rest_framework import serializers
from its_regions_2025.models import (
    User,
    TypeObject,
    Object,
    Priority,
    Status,
    Task,
    TypeBreaking,
    TypeQuality,
)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class LogoutSerializer(serializers.Serializer):
    pass


class TypeObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeObject
        fields = ["id", "name"]


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = ["id", "name", "type", "longitude", "latitude"]


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ["id", "name"]


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]


class TypeBreakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeBreaking
        fields = ["id", "name"]


class TypeQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeQuality
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "priority",
            "status",
            "object",
            "executor",
            "creator",
            "quality_report",
            "start_date",
            "deadline",
            "text_report",
            "description",
            "diagnostic_data",
            "result",
            "was_done",
            "name_component",
            "type_breaking",
        ]
