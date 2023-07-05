from tkinter import S
from rest_framework.permissions import BasePermission, SAFE_METHODS

from project.models import Contributors, Project

EDIT_METHODES = ("DELETE", "PACTH")


class IsAuthor(BasePermission):
    def is_author(self, request, obj):
        if request.user == obj.author_user_id:
            return True


class IsCollaborator(BasePermission):
    def is_collaborator(self, request, obj):
        collaborators = Contributors.objects.filter(project_id=obj)
        if request.user in collaborators:
            return True


class ProjectPermission(IsAuthor, IsCollaborator):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if self.is_author(request=request, obj=obj):
            True
        if request.method not in EDIT_METHODES:
            if self.is_collaborator(request=request, obj=obj):
                return True
        return False


class CollaboratorPermission(IsAuthor):
    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs["project_pk"])
        if self.is_author(request=request, obj=project):
            return True
        if self.is_collaborator(request=request, obj=project.id):
            return True

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class IssuePermission(IsAuthor, IsCollaborator):
    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs["project_pk"])
        if self.is_author(request=request, obj=project):
            return True
        if self.is_collaborator(request=request, obj=project.id):
            return True

    def has_object_permission(self, request, view, obj):
        if self.is_author(request=request, obj=obj):
            return True
        if request.method in SAFE_METHODS and self.is_collaborator(request=request, obj=obj.project_id):
            True


class CommentPermission(IsAuthor, IsCollaborator):
    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs["project_pk"])
        if self.is_author(request=request, obj=project):
            return True
        if self.is_collaborator(request=request, obj=project.id):
            return True

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
