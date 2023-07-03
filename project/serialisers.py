from re import T
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, PrimaryKeyRelatedField
from django.db.models import Q
from authentication.models import User

from .models import Comments, Contributors, Issues, Project


class ProfileUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class ContributorSerializer(ModelSerializer):
    user_info = ProfileUserSerializer(source="user_id", read_only=True)
    project_id = PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False)

    class Meta:
        model = Contributors
        fields = [
            "id",
            "user_id",
            "user_info",
            "permission",
            "project_id",
            "role",
        ]

    def validate(self, data):
        # Verification si le collaborateur est deja inscrit au projet.
        if Contributors.objects.filter(Q(project_id=data["project_id"]) & Q(user_id=data["user_id"])).exists():
            raise ValidationError("Collaborator already exits in project")
        return data


class CommentsListSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        "issue_pk": "issue__pk",
        "project_pk": "issue__project__pk",
    }
    project = SerializerMethodField()
    author_user_id = ProfileUserSerializer()

    class Meta:
        model = Comments
        fields = ["id", "author_user_id", "description", "issues_id"]


class CommentsDetailSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class IssuesListSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        "project_pk": "project__pk",
    }
    author_user_id = ProfileUserSerializer()

    class Meta:
        model = Issues
        fields = ["id", "title", "tag", "priority", "project_id", "author_user_id", "status"]


class IssuesDetailSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"


class ProjectListSerializer(ModelSerializer):
    author_user_id = PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    author_info = ProfileUserSerializer(source="author_user_id", read_only=True)

    class Meta:
        model = Project
        fields = ["id", "title", "type", "author_user_id", "author_info", "time_created"]

    def validate_title(self, value):
        # Nous vérifions que la projet existe
        if Project.objects.filter(title=value).exists():
            raise ValidationError("Project already exists")
        return value


class ProjectDetailSerializer(ModelSerializer):
    contributors = ContributorSerializer(source="contributors_set", many=True)
    author_info = ProfileUserSerializer(source="author_user_id", read_only=True)
    issues = IssuesListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "type",
            "description",
            "author_user_id",
            "author_info",
            "contributors",
            "issues",
            "time_created",
        ]
