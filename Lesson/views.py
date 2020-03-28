from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.
from Lesson.models import Category, Lesson, LessonMaterial, SubCategory, UserLesson
from Lesson.permissions import IsActiveAndIsAuthenticated
from Lesson.serializers import CategorySerializer, SubCategorySerializer, LessonSerializer, RetrieveCategorySerializer, \
    RetrieveSubCategorySerializer, RetrieveLessonSerializer, HomeworkSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve':
            return RetrieveCategorySerializer
        return CategorySerializer


class SubCategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        print(self.action)
        if self.action == 'retrieve':
            return RetrieveSubCategorySerializer
        return SubCategorySerializer


class LessonViewSet(ReadOnlyModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsActiveAndIsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve':
            return RetrieveLessonSerializer
        return LessonSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        is_in_cart = UserLesson.objects.filter(sub_category=instance.sub_category).filter(user=request.user).first()
        if is_in_cart:
            homework = is_in_cart.homework.all()
            homework_serializer = HomeworkSerializer(homework, many=True).data
            data = serializer.data
            data["homeworks"] = homework_serializer
            return Response(data)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "у вас нету доступа к уроку"})
