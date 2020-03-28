from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import Category, Lesson, SubCategory, LessonMaterial, Homework


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class LessonMaterialSerializer(ModelSerializer):
    class Meta:
        model = LessonMaterial
        fields = '__all_'


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'description', 'image')


class HomeworkSerializer(ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'


class RetrieveLessonSerializer(ModelSerializer):
    lesson_materials = LessonMaterialSerializer(many=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonSmallSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name', 'description', 'image')


class RetrieveSubCategorySerializer(ModelSerializer):
    lessons = LessonSmallSerializer(many=True)

    class Meta:
        model = SubCategory
        fields = '__all__'


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class RetrieveCategorySerializer(ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
