from rest_framework.permissions import BasePermission, SAFE_METHODS

from project.models import Contributors, Project

EDIT_METHODES = ("DELETE", "PACTH")


class IsAuthor(BasePermission):
    # Define if user connected is author of object

    def is_author(self, request, obj):
        if request.user == obj.author_user_id:
            return True


class IsCollaborator(BasePermission):
    # define if user connected is a project collaborators

    def is_collaborator(self, request, obj):
        collaborators = Contributors.objects.filter(project_id=obj)
        if request.user in collaborators:
            return True


class ProjectPermission(IsAuthor, IsCollaborator):
    """Define permissions for project.
    A user authenticated can see all project, and create a new project.
    Deleting or updating a project is reserved for the project author.
    Superuser have fullaccess.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if self.is_author(request=request, obj=obj):
            return True
        if request.method not in EDIT_METHODES and self.is_collaborator(request=request, obj=obj):
            return True
        return False


class CollaboratorPermission(IsAuthor):
    """Define permissions for project contributors.
    Only Author and collabarator of project can see collaborators of project.
    Only Author can to add and deleting a collaborator.
    Superuser have fullaccess.
    """

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs["project_pk"])
        if request.user.is_superuser:
            return True
        if self.is_author(request=request, obj=project):
            return True
        if request.method in SAFE_METHODS and self.is_collaborator(request=request, obj=project.id):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if self.is_author(request=request, obj=obj):
            return True
        if request.method in SAFE_METHODS and self.is_collaborator(request=request, obj=obj.id):
            return True


class IssuePermission(IsAuthor, IsCollaborator):
    """Define permissions for issue of project.
    The project author and contributors can access the project problem and create new project-related problems.
    Deleting or updating a probleme is reserved for the probleme author.
    Superuser have fullaccess.
    """

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs["project_pk"])
        if request.user.is_superuser:
            return True
        if self.is_author(request=request, obj=project):
            return True
        if self.is_collaborator(request=request, obj=project.id):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if self.is_author(request=request, obj=obj):
            return True
        if request.method in SAFE_METHODS and self.is_collaborator(request=request, obj=obj.project_id):
            True


class CommentPermission(IsAuthor, IsCollaborator):
    """Define permissions for comments of issue.
    Only project contributors and comment author can acces and create issue comments.
    Only author of comment can deleting and updating a comment.
    Superuser have fullaccess.
    """

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs["project_pk"])
        if request.user.is_superuser:
            return True
        if self.is_author(request=request, obj=project):
            return True
        if self.is_collaborator(request=request, obj=project.id):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if self.is_author(request=request, obj=obj):
            return True
        if request.method in SAFE_METHODS and self.is_collaborator(request=request, obj=obj.issues_id.project_id):
            return True
