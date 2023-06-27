from rest_framework.serializers import ModelSerializer

from .models import Comments, Issues, Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "type", "author_user_id", "staff", "time_created"]

        def get_issues(self, instance):
            # Le paramètre 'instance' est l'instance de la projet consultée.
            # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
            # d'entités dans la liste
            # On applique le filtre sur notre queryset pour n'avoir que les probleme actifs
            queryset = instance.issues.all()
            # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
            serializer = IssuesSerializer(queryset, many=True)
            # la propriété '.data' est le rendu de notre serializer que nous retournons ici
            return serializer.data


class CommentsSerializer(ModelSerializer):
    class Meta:
        model: Comments
        fields = "__all__"


class IssuesSerializer(ModelSerializer):
    class Meta:
        model: Issues
        fields = "__all__"
