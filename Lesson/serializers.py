from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import Category, Lesson, SubCategory, LessonMaterial


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all_'


class LessonMaterialSerializer(ModelSerializer):
    class Meta:
        model = LessonMaterial
        fields = '__all_'


class LessonSerializer(ModelSerializer):
    lesson_materials = LessonMaterialSerializer(many=True)

    class Meta:
        model = Lesson
        fields = '__all_'
