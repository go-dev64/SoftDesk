from rest_framework.serializers import ModelSerializer

from .models import Comments, Issues, Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "type", "description", "time_created"]


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"
