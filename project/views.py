from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet
from django.db.models import Q


from .models import Comments, Contributors, Issues, Project
from .permisssions import CommentPermission, IssuePermission, ProjectPermission
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
    permission_classes = [IsAuthenticated, ProjectPermission]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = self.request.user.id
        request.POST._mutable = False
        return super(ProjectViewset, self).create(request, *args, **kwargs)

    def get_queryset(self):
        """return les projes dans lesquels user a participé

        Returns:
            _type_: _description_
        """

        return Project.objects.all().order_by("title")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserViews(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project_id"] = self.kwargs["project_pk"]
        request.POST._mutable = False
        return super(UserViews, self).create(request, *args, **kwargs)

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs["project_pk"])
        return Contributors.objects.filter(project_id=project.pk).order_by("id")


class IssuesView(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """

    serializer_class = IssuesListSerializer
    detail_serializer_class = IssuesDetailSerializer
    permission_classes = [IsAuthenticated, IssuePermission]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = str(self.request.user.pk)
        request.data["project_id"] = self.kwargs["project_pk"]
        request.POST._mutable = False
        print(request.data)
        return super(IssuesView, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs["project_pk"])

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()


class CommentsViews(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """

    serializer_class = CommentsListSerializer
    detail_serializer_class = CommentsDetailSerializer
    permission_classes = [IsAuthenticated, CommentPermission]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = str(self.request.user.pk)
        request.data["issue_id"] = self.kwargs["issue_pk"]
        request.POST._mutable = False
        return super(CommentsViews, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs["issue_pk"])

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()
