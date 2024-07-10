from rest_framework import serializers

from .models import User, Task, Comment, TaskList


# extra_kwargs allows you to customize individual field behaviors.
#  write_only ensures it is not exposed in API responses, enhancing security.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "complete_status",
            "assigned_to",
            "attachment",
        ]

    read_only_fields = ["id", "created_by"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content"]
        read_only_fields = ["created_at", "author"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = ["id", "name", "owner", "is_public", "tasks"]
        read_only_fields = ["id", "owner"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)
