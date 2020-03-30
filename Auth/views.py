from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import CreateAndIsAuthenticated
from .serializers import UserReadSerializer, UserWriteSerializer, LoginSerializer
from .models import MyUser


class UserViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserReadSerializer
    queryset = MyUser.objects.all()
    permission_classes = [CreateAndIsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = MyUser.objects.get(id=serializer.data["id"])
        token = RefreshToken.for_user(user)
        print(user)
        data = serializer.data
        data["token"] = str(token.access_token)
        data["password"] = ""
        print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return UserReadSerializer
        return UserWriteSerializer

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        user_serializer = UserReadSerializer(request.user)
        data = user_serializer.data
        return Response(status=200, data={'user': data})

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        password = serializer.data['password']
        user = authenticate(username=username, password=password)
        if not user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "не правильные логин или пароль"})
        token = RefreshToken.for_user(user=user)
        user_serializer = UserReadSerializer(user)
        data = user_serializer.data
        data["password"] = ""
        data["token"] = str(token.access_token)
        return Response(status=200, data={'user': data})
