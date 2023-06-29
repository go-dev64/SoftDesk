from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField

from authentication import serializers

from .models import Comments, Issues, Project
from authentication.serializers import UserSerializer


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "type", "author_user_id", "time_created"]

    def validate_title(self, value):
        # Nous vérifions que la projet existe
        if Project.objects.filter(title=value).exists():
            raise ValidationError("Project already exists")
        return value


class ProjectDetailSerializer(ModelSerializer):
    staff = SerializerMethodField()

    def get_staff(self, instance):
        queryset = instance.contributors_set.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Project
        fields = ["id", "title", "type", "description", "author_user_id", "staff", "time_created"]


class CommentsListSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ["id", "author_user_id", "description", "issues_id"]


class CommentsDetailSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class IssuesListSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = ["id", "title", "tag", "priority", "project_id", "status"]


class IssuesDetailSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"
