from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, PrimaryKeyRelatedField

from authentication.models import User

from .models import Comments, Contributors, Issues, Project


class ProfileUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class ContributorSerializer(ModelSerializer):
    """Serilaizer of contributor

    Args:
        ModelSerializer (_type_): _description_
    """

    user_id = SerializerMethodField()
    project_id = PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Contributors
        fields = ["user_id", "permission", "role", "project_id"]

    def get_user_id(self, instance):
        user = instance.user_id
        serializer = ProfileUserSerializer(user)
        return serializer.data

    def create(self, validated_data):
        user_data = validated_data.pop("user_id")
        user = User.objects.get(id=user_data["id"])
        permission = validated_data.get("permission")
        role = validated_data.get("role")
        project_id = validated_data.get("project_id")

        contributor = Contributors.objects.create(
            user=ProfileUserSerializer(user), permission=permission, role=role, project_id=project_id
        )
        return contributor


class ProjectListSerializer(ModelSerializer):
    author_user_id = ProfileUserSerializer()

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
    author_user_id = ProfileUserSerializer()

    class Meta:
        model = Project
        fields = ["id", "title", "type", "description", "author_user_id", "contributors", "time_created"]


class CommentsListSerializer(ModelSerializer):
    project = SerializerMethodField()
    author_user_id = ProfileUserSerializer()

    class Meta:
        model = Comments
        fields = ["id", "author_user_id", "description", "issues_id"]


class CommentsDetailSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class IssuesListSerializer(ModelSerializer):
    author_user_id = ProfileUserSerializer()

    class Meta:
        model = Issues
        fields = ["id", "title", "tag", "priority", "project_id", "author_user_id", "status"]


class IssuesDetailSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"
