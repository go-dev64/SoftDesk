from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from .models import Project
from .serialisers import ProjectSerializer


class ProjectViewset(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
