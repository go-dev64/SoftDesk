from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField
from django.db.models import Q
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
    Args:
        ModelSerializer (_type_): _description_

    Raises:
        ValidationError: "Collaborator already exits in project"

    Returns:
        _type_: _description_
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

    def validate(self, data):
        # Verification si le collaborateur est deja inscrit au projet.
        if Contributors.objects.filter(Q(project_id=data["project_id"]) & Q(user_id=data["user_id"])).exists():
            raise ValidationError("Collaborator already exits in project")
        return data


class CommentsListSerializer(ModelSerializer):
    """Serializer for list of comment of issue of project.
    Add a embedded serializer (ProfileUserSerializer), read only, for display user frist name and last_name.
    Args:
        ModelSerializer (_type_): _description_
    """

    author_info = ProfileUserSerializer(source="author_user_id", read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "author_user_id", "author_info", "description", "issue_id"]


class CommentsDetailSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class IssuesListSerializer(ModelSerializer):
    """Serializer for list of Issues.
    Add a embedded serializer (ProfileUserSerializer), read only, for display author and assignee_user frist name and last_name.
    Args:
        ModelSerializer (_type_): _description_

    Raises:
        ValidationError: Issue already exits in project

    Returns:
        _type_: _description_
    """

    author_info = ProfileUserSerializer(source="author_user_id", read_only=True)
    assignee_user_id = PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    assignee_user_info = ProfileUserSerializer(source="author_user_id", read_only=True)
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
        # Nous vérifions si le probleme existe
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
    Args:
        ModelSerializer (_type_): _description_

    Raises:
        ValidationError: _description_

    Returns:
        _type_: _description_
    """

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
    contributors = ContributorSerializer(source="project_contributors", many=True)
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
