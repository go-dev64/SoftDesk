from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from rest_framework.response import Response

from .serializers import UserSerializer


class CreateUserView(ModelViewSet):
    serializer_class = UserSerializer

    def post_queryset(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
