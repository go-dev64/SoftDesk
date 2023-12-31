from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField
from authentication.models import User

from .models import Comments, Contributors, Issues, Project


class ProfileUserSerializer(ModelSerializer):
    # embedded serializer for displaying user first name and last name
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class ContributorSerializer(ModelSerializer):
    """Serilizer for contibutor project.
    Add a embedded serializer (ProfileUserSerializer), read only, for display user frist name and last_name.
    """

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


class CommentsListSerializer(ModelSerializer):
    """Serializer for list of comment of issue of project.
    Add a embedded serializer (ProfileUserSerializer), read only, for display user frist name and last_name.
    """

    author_info = ProfileUserSerializer(source="author_user_id", read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "author_user_id", "author_info", "description", "issue_id"]


class CommentsDetailSerializer(ModelSerializer):
    author_info = ProfileUserSerializer(source="author_user_id", read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "author_user_id", "author_info", "description", "issue_id"]


class IssuesListSerializer(ModelSerializer):
    """Serializer for list of Issues.
    Add a embedded serializer (ProfileUserSerializer),
    read only, for display author and assignee_user frist name and last_name.
    """

    author_info = ProfileUserSerializer(source="author_user_id", read_only=True)
    assignee_user_info = ProfileUserSerializer(source="assignee_user_id", read_only=True)
    project_id = PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False)

    class Meta:
        model = Issues
        fields = [
            "id",
            "title",
            "tag",
            "priority",
            "author_user_id",
            "author_info",
            "assignee_user_id",
            "assignee_user_info",
            "project_id",
            "status",
        ]

    def validate_title(self, value):
        # Check if Issue already exist.
        if Issues.objects.filter(title=value).exists():
            raise ValidationError("Issue already exits in project!")
        return value


class IssuesDetailSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"


class ProjectListSerializer(ModelSerializer):
    """Serializer for project list.
    Add a embedded serializer (ProfileUserSerializer), read only, for display author frist name and last_name.
    """

    author_user_id = PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    author_info = ProfileUserSerializer(source="author_user_id", read_only=True)

    class Meta:
        model = Project
        fields = ["id", "title", "type", "author_user_id", "author_info", "time_created"]

    def validate_title(self, value):
        # Check if project already exist.
        if Project.objects.filter(title=value).exists():
            raise ValidationError("Project already exists")
        return value

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        Contributors.objects.create(user_id=project.author_user_id, project_id=project, role="R", permission="t")
        return project


class ProjectDetailSerializer(ModelSerializer):
    contributors = ContributorSerializer(source="project_contributors", many=True)
    author_info = ProfileUserSerializer(source="author_user_id", read_only=True)

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
