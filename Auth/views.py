import uuid

from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import CreateAndIsAuthenticated
from .serializers import UserReadSerializer, UserWriteSerializer, LoginSerializer, GeneratePassword, \
    TokenCheckForgetPassword, ForgotPassword
from .models import MyUser
from django.core.cache import cache
from django.core.cache import cache

from .tasks import send_forgot_email


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
        # MyUser.objects.filter(activationchange__group_names=)
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

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def generate_forgot_password(self, request, *args, **kwargs):
        serializer = GeneratePassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = MyUser.objects.filter(email__exact=email)
        if len(user) <= 0:
            return Response(status=404, data={'error': 'user not found'})
        user = user.first()
        token = uuid.uuid4()
        print("user_forgot_token_%s" % token)
        c = cache.set("user_forgot_token_%s" % token, str(user.id), timeout=500)
        print(cache.get("user_forgot_token_%s" % token, None))
        send_forgot_email(user_id=user.id, token=token)
        return Response(status=200, data={'ok': 'ok'})

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def check_forgot_password_token(self, request, *args, **kwargs):
        serializer = TokenCheckForgetPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data['token']
        print("user_forgot_token_%s" % token)
        user_id = cache.get("user_forgot_token_%s" % token, None)
        print(user_id)
        user = MyUser.objects.filter(id=user_id)
        if len(user) <= 0:
            return Response(status=404, data={'error': 'user not found'})
        return Response(status=200, data={'ok': 'ok'})

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def set_new_password(self, request, *args, **kwargs):
        serializer = ForgotPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data['token']
        password = serializer.data['password']
        user_id = cache.get("user_forgot_token_%s" % token, None)
        user = MyUser.objects.filter(id=user_id)
        if len(user) <= 0:
            return Response(status=404, data={'error': 'user not found'})
        user = user.first()
        user.set_password(raw_password=password)
        user.save()
        return Response(status=200, data={'ok': 'ok'})


def verify(request, uuid):
    try:
        user = MyUser.objects.get(verification_uuid=uuid, is_verified=False)
    except MyUser.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_verified = True
    user.save()

    return redirect('https://yessenov-online.kz')
