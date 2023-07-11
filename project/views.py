from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from authentication.models import User
from .models import Comments, Contributors, Issues, Project
from .permisssions import ContributorPermission, CommentPermission, IssuePermission, ProjectPermission
from .serialisers import (
    CommentsDetailSerializer,
    CommentsListSerializer,
    ContributorSerializer,
    IssuesDetailSerializer,
    IssuesListSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
)


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

    def _check_user_exits(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.pk)

        return user

    def _check_user_is_project_contributor(self, request, obj, *args, **kwargs):
        contributors = Contributors.objects.filter(project_id=self.kwargs["project_pk"], user_id=request.user.pk)
        self.check_object_permisssions(self, request, obj)
        return contributors


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    """Management view of Project.
    the author of new project, user connected, is automatically filled in.

    Args:
        MultipleSerializerMixin (_type_): _description_
        ModelViewSet (_type_): _description_

    Returns:
        _type_: _description_
    """

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def create(self, request, *args, **kwargs):
        # Modify the request.data so that the author is automatically defined.

        request.POST._mutable = True
        request.data["author_user_id"] = self.request.user.id
        request.POST._mutable = False
        return super(ProjectViewset, self).create(request, *args, **kwargs)

    def get_queryset(self):
        # return all project sorted by title.
        return Project.objects.all().order_by("title")


class UserViews(MultipleSerializerMixin, ModelViewSet):
    """Management view of Contributors of project.
    The project to which the user is added is automatically filled in.


    Args:
        ModelViewSet (_type_): _description_
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]

    def create(self, request, *args, **kwargs):
        # check if user exits and if is already exist in project contributor.
        try:
            self._check_user_exits(request=request)
            contributors = self._check_user_is_project_contributor(request=request)
            if contributors.exists():
                raise ValidationError("Collaborator already exists in project.")

        except User.DoesNotExist:
            raise ValidationError("User does not exist")

        else:
            # Modify the request.data so that the project_id is automatically defined.
            request.POST._mutable = True
            request.data["project_id"] = self.kwargs["project_pk"]
            request.POST._mutable = False
            return super(UserViews, self).create(request, *args, **kwargs)

    def get_queryset(self):
        # return all contributor sorted by id.
        project = Project.objects.get(id=self.kwargs["project_pk"])
        return Contributors.objects.filter(project_id=project.pk).order_by("id")


class IssuesView(MultipleSerializerMixin, ModelViewSet):
    """Management view of Issue.
    The author issue, user connected, and the project of issue are automatically filled in.

    Args:
        MultipleSerializerMixin (_type_): _description_
        ModelViewSet (_type_): _description_

    Returns:
        _type_: _description_
    """

    serializer_class = IssuesListSerializer
    detail_serializer_class = IssuesDetailSerializer
    permission_classes = [IsAuthenticated, IssuePermission]

    def create(self, request, *args, **kwargs):
        # check if user exits and if is project contributor.
        try:
            self._check_user_exits(request=request)
            self._check_user_is_project_contributor(request=request)

        except User.DoesNotExist:
            raise ValidationError("User assignee does not exist")

        except Contributors.DoesNotExist:
            raise ValidationError("the assigned user must be a contributor to the project.")

        else:
            # Modify the request.data so that the project_id and author_user_id are automatically defined.
            request.POST._mutable = True
            request.data["author_user_id"] = self.request.user.pk
            request.data["project_id"] = self.kwargs["project_pk"]
            request.POST._mutable = False
            return super(IssuesView, self).create(request, *args, **kwargs)

    def get_queryset(self):
        # return all Issue sorted by title.
        return Issues.objects.filter(project_id=self.kwargs["project_pk"]).order_by("title")


class CommentsViews(MultipleSerializerMixin, ModelViewSet):
    """Management view of comments.
    The author comment, user connected, and the isssue of comment are automatically filled in.

    Args:
        MultipleSerializerMixin (_type_): _description_
        ModelViewSet (_type_): _description_

    Returns:
        _type_: _description_
    """

    serializer_class = CommentsListSerializer
    detail_serializer_class = CommentsDetailSerializer
    permission_classes = [IsAuthenticated, CommentPermission]

    def create(self, request, *args, **kwargs):
        # Modify the request.data so that the author__useer_id and issue_id are automatically defined.
        request.POST._mutable = True
        request.data["author_user_id"] = str(self.request.user.pk)
        request.data["issue_id"] = self.kwargs["issue_pk"]
        request.POST._mutable = False
        return super(CommentsViews, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs["issue_pk"])
