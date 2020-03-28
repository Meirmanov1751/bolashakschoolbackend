from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.
from Lesson.models import Category, Lesson, LessonMaterial, SubCategory
from Lesson.serializers import CategorySerializer, SubCategorySerializer, LessonSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SubCategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


class LessonViewSet(ReadOnlyModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
