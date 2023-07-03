from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, PrimaryKeyRelatedField
from django.db.models import Q
from authentication.models import User

from .models import Comments, Contributors, Issues, Project


class ProfileUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class ContributorSerializer(ModelSerializer):
    project_id = PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Contributors
        fields = ["user_id", "permission", "role", "project_id"]

    def validate_new_colaborator(self, value):
        print(value, "toto")
        # Nous vérifions que la projet existe
        if Contributors.objects.filter(Q(project_id=self.kwargs["project_pk"]) | Q(user_id=value)).exists():
            raise ValidationError("Colaborator already exits in project")
        return value


class ProjectListSerializer(NestedHyperlinkedModelSerializer):
    author_user_id = PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

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
