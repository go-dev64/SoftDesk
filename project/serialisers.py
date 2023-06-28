from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField

from .models import Comments, Issues, Project


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "type", "author_user_id", "time_created"]

    def validate_title(self, value):
        # Nous vérifions que la projet existe
        if Project.objects.filter(title=value).exists():
            raise ValidationError("Category already exists")
        return value


class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "type", "description", "author_user_id", "time_created"]


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"
