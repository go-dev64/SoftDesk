from django.urls import path, include
from rest_framework_nested import routers

from .views import ProjectViewset, IssuesView, CommentsViews, UserViews

router = routers.DefaultRouter()
router.register(r"projects", ProjectViewset, basename="projects")
"""Generate project/{pk}"""


project_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
project_router.register(r"users", UserViews, basename="project-users")

project_router.register(r"issues", IssuesView, basename="project-issues")

issues_router = routers.NestedSimpleRouter(project_router, r"issues", lookup="issue")
issues_router.register(r"comments", CommentsViews, basename="comments")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(project_router.urls)),
    path("", include(issues_router.urls)),
]
