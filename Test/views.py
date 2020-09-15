from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import TestTasks, TestGroup, TestCategory, TestGroupCategory, TestGroupUser
from .permissions import HasTestAccessGroupCategory, HasTestAccessGroup
from .serializers import TestCategorySerializer, TestGroupDetailedSerializer, TestGroupCategoryDetailedSerializer, \
    TestCategoryPriceSerializer


# Create your views here.
class TestCategoryViewSet(ReadOnlyModelViewSet):
    queryset = TestCategory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TestCategorySerializer


class TestGroupViewSet(ReadOnlyModelViewSet):
    queryset = TestGroup.objects.all()
    permission_classes = [IsAuthenticated, HasTestAccessGroup]
    serializer_class = TestGroupDetailedSerializer


class TestGroupCategoryViewSet(ReadOnlyModelViewSet):
    queryset = TestGroupCategory.objects.all()
    permission_classes = [IsAuthenticated, HasTestAccessGroupCategory]
    serializer_class = TestGroupCategoryDetailedSerializer


class TestCategoryPriceViewSet(ReadOnlyModelViewSet):
    queryset = TestCategory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TestCategoryPriceSerializer

    @action(methods=['post'], detail=False)
    def add(self, request, *args, **kwargs):
        data = request.data
        if 'test_group' in data:
            test_group_id = data['test_group']
            test_group = TestGroup.objects.filter(id=test_group_id)
            if test_group.exists():
                test_group = test_group.first()
                test_user = TestGroupUser.objects.create(user=request.user, group=test_group)
                request.user.testgroupuser_set.add(test_user)
                return Response({'id': test_user.id})
        return Response({'asd': 'asd'})

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def verify(self, request, *args, **kwargs):
        data = request.data
        if 'test_group' in data:
            test_group_id = data['test_group']
            test_group = TestGroupUser.objects.filter(id=test_group_id)
            if test_group.exists():
                test_group = test_group.first()
                test_group.verified = True
                test_group.save()
                return Response({'ok': 'ok'})
        return Response({'asd': 'asd'})
