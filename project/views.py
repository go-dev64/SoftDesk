from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


from .models import Project
from .serialisers import ProjectSerializer


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewset, self).create(request, args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        else:
            return Project.objects.all()
