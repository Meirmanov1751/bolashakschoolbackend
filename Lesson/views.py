from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.
from Analytics.models import AnalyticsLesson
from Auth.models import UserGroups, MyUser
from Lesson.models import Category, Lesson, LessonMaterial, SubCategory, UserLesson
from Lesson.permissions import IsActiveAndIsAuthenticated
from Lesson.serializers import CategorySerializer, SubCategorySerializer, LessonSerializer, RetrieveCategorySerializer, \
    RetrieveSubCategorySerializer, RetrieveLessonSerializer, HomeworkSerializer, SubCategorySerializerWithImageUrl
from Lesson.vimoe import getOtp


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user_groups = UserGroups.objects.filter(users=self.request.user)
        sub_categories = user_groups.values_list('sub_category__id', flat=True)
        pk = self.kwargs['pk']
        category = Category.objects.filter(pk=pk).filter(sub_categories__in=sub_categories)
        sub_categories_list = category.values_list('sub_categories', flat=True)
        sub_categories = SubCategory.objects.filter(id__in=sub_categories_list)
        sub_categories_serializer = SubCategorySerializerWithImageUrl(sub_categories, many=True,  context={"request": self.request})
        print(sub_categories_serializer.data)
        data = serializer.data
        data["sub_categories"] = []

        if category.count() > 0:
            data["sub_categories"] = sub_categories_serializer.data
        return Response(data)


    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve':
            return RetrieveCategorySerializer
        return CategorySerializer


class SubCategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            user = self.request.user
            user_groups = UserGroups.objects.filter(users=user).first()
            return user_groups.sub_category
        return SubCategory.objects.all()

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
        # analytics_lesson = AnalyticsLesson.objects.filter(user=request.user).filter(lesson=instance)
        # if len(analytics_lesson) == 0:
        #     AnalyticsLesson.objects.create(user=request.user, lesson=instance)

        is_in_cart = UserGroups.objects.filter(sub_category=instance.sub_category).filter(users=request.user).first()
        if is_in_cart:
            # homework = is_in_cart.homework.all()
            # homework_serializer = HomeworkSerializer(homework, many=True).data
            data = serializer.data
            # if(data["videoId"]):
            #     otp = getOtp(data["videoId"])
            #     data["otp"] = otp
            # data["homeworks"] = homework_serializer
            return Response(data)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "у вас нету доступа к уроку"})
