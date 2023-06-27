from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import UserSerializer
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import User


class CreateUserView(ViewSet):
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
