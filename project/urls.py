from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import ProjectViewset

router = routers.SimpleRouter()

router.register("projects", ProjectViewset, basename="projects")

urlpatterns = [path("", include(router.urls))]
