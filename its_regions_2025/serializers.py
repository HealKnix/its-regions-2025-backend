from rest_framework import serializers
import its_regions_2025.models as models


class AuthenticatedSerializer(serializers.Serializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "is_staff",
            "email",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = models.User
        fields = [
            "email",
            "password",
        ]


class LogoutSerializer(serializers.Serializer):
    pass


class TypeObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeObject
        fields = ["id", "name"]


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Object
        fields = ["id", "name", "type", "longitude", "latitude"]


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Priority
        fields = ["id", "name"]


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = ["id", "name"]


class TypeBreakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeBreaking
        fields = ["id", "name"]


class TypeQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeQuality
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "password",
            "is_superuser",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
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


class TaskVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskVersion
        fields = [
            "id",
            "version_uuid",
            "task",
            "field",
            "value",
            "user",
            "updated_at",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = [
            "id",
            "task",
            "user",
            "title",
            "message",
            "created_at",
            "is_read",
            "is_deleted",
        ]
