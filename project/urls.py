from django.contrib import admin
from django.urls import path, include

from .views import ProjectAPIView

urlpatterns = [path("api/category/", ProjectAPIView.as_view())]
