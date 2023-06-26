from rest_framework.serializers import ModelSerializer

from .models import Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        """
        docstring
        """

        model = Project
        fields = ["__all__"]
