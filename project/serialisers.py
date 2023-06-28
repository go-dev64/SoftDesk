from rest_framework.serializers import ModelSerializer, SerializerMethodField

from authentication import serializers

from .models import Comments, Issues, Project


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "type", "author_user_id", "time_created"]


class ProjectDetailSerializer(ModelSerializer):
    staff = SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "title", "type", "description", "author_user_id", "time_created"]

    def get_staff(self, instance):
        # Le paramètre 'instance' est l'instance du project consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        queryset = instance.staff.all()
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProjectDetailSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"
