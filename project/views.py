from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Project
from .serialisers import ProjectListSerializer, ProjectDetailSerializer


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    # permission_classes = [IsAuthenticated]

    """def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user
        request.POST._mutable = False
        print(request.data)
        return super(ProjectViewset, self).create(request, *args, **kwargs)"""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author_user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """return les projet dans les quels user a participé

        Returns:
            _type_: _description_
        """
        if self.request.user.is_superuser:
            return Project.objects.all()
        else:
            return Project.objects.filter(Q(author_user_id=self.request.user))

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()
