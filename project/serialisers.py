from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField

from authentication.models import User

from .models import Comments, Contributors, Issues, Project


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ["user_id", "permission", "role"]


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
    contributors = ContributorSerializer(source="contributors_set", many=True)

    class Meta:
        model = Project
        fields = ["id", "title", "type", "description", "author_user_id", "contributors", "time_created"]


class CommentsListSerializer(ModelSerializer):
    project = SerializerMethodField()

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
        fields = ["id", "title", "tag", "priority", "project_id", "author_user_id", "status"]


class IssuesDetailSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"
