from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

import project

from .models import Contributors, Issues, Project
from .serialisers import (
    CommentsDetailSerializer,
    CommentsListSerializer,
    ContributorSerializer,
    IssuesDetailSerializer,
    IssuesListSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
)


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    """def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.POST._mutable = False
        print(request.data)
        return super(ProjectViewset, self).create(request, *args, **kwargs)"""

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author_user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """return les projes dans lesquels user a participé

        Returns:
            _type_: _description_
        """
        if self.request.user.is_superuser:
            return Project.objects.all()
        else:
            # return Project.objects.filter(Q(author_user_id=self.request.user) | Q)
            return Project.objects.filter(
                Q(author_user_id=self.request.user) | Q(contributors=self.request.user.pk)
            ).order_by("-time_created")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()


class IssuesView(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """

    serializer_class = IssuesListSerializer
    detail_serializer_class = IssuesDetailSerializer

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs["project_pk"]
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.project = project_id
        # assingnee_user =
        serializer.save(author_user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Issues.objects.filter(project=self.kwargs["project_pk"])

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()


class CommentsViews(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """

    pass


class UserViews(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """

    serializer_class = ContributorSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributors.objects.filter(project=self.kwargs["project_pk"])

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(self.kwargs["project_pk"])
        """if project.author_user_id is not request.user:
            raise ValueError("Vous n'etes pas le responsable du projet. Ajout de collaborateur impossible.")"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.project_id = project
        serializer.save()
        return super().create(request, *args, **kwargs)
