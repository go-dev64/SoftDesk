from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import ProjectViewset

router = routers.SimpleRouter()

router.register("project", ProjectViewset, basename="project")

urlpatterns = [path("api/", include(router.urls))]
