from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def is_author(self, request, obj):
        if request.user is obj.author_user_id:
            return True


class isCollaborator(BasePermission):
    def is_author(self, request, project):
        if request.user in project.user_id_set:
            return True
