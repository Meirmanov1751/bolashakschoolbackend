from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework_simplejwt.tokens import RefreshToken

from Auth.models import MyUser
from .permissions import HasLessonAccess
from .serializers import CourseSerializer, CategoryDetailedSerializer, ModuleDetailedSerializer, \
    LessonDetailedSerializer, LessonUserHistorySerializer, CoursePriceSerializer
from .models import Category, Course, LessonTasks, Lesson, Module, LessonUserHistory, ModuleUser


class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryDetailedSerializer


class ModuleViewSet(ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ModuleDetailedSerializer


class CoursePriceViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CoursePriceSerializer

    @action(methods=['post'], detail=False)
    def add(self, request, *args, **kwargs):
        data = request.data
        if 'module' in data:
            module_id = data['module']
            module = Module.objects.filter(id=module_id)
            if module.exists():
                module = module.first()
                module_user = ModuleUser.objects.create(user=request.user, module=module)
                request.user.moduleuser_set.add(module_user)
                return Response({'id': module_user.id})
        return Response({'asd': 'asd'})

    @action(methods=['post'], detail=False, permission_classes[AllowAny])
    def verify(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        if 'module' in data:
            module_id = data['module']
            module = ModuleUser.objects.filter(id=module_id)
            if module.exists():
                module = module.first()
                module.verified = True
                module.save()
                return Response({'id': module.id})
        return Response({'asd': 'asd'})


class LessonViewSet(ReadOnlyModelViewSet):
    queryset = Lesson.objects.all().order_by('lesson_order')
    permission_classes = [IsAuthenticated, HasLessonAccess]
    serializer_class = LessonDetailedSerializer

    @action(methods=['post'], detail=True)
    def history(self, request, *args, **kwargs):
        lesson = Lesson.objects.filter(pk=kwargs['pk'])
        print(request.data)
        if len(lesson) <= 0:
            return Response(status=404, data={'message': 'Lesson not found'})
        else:
            lesson = lesson.first()
            history = LessonUserHistory.objects.filter(lesson=lesson, user=request.user)
            if len(history) <= 0:
                history = LessonUserHistory.objects.create(user=request.user, lesson=lesson)
            else:
                history = history.first()
            if 'mark' in request.data:
                history.mark = request.data.get("mark", 0)
            history.visited_count += 1
            history.save()
            print('view history', history.user)
            return Response(LessonUserHistorySerializer(history).data)
        return Response({'asd': 'asd'})
