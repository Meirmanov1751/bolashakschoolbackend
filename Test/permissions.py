from rest_framework import permissions

from Course.models import Lesson, Category, Module
from Test.models import TestGroup, TestGroupCategory


class HasTestAccessGroup(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_object_permission(self, request, view, obj):
        test_group = obj.testgroupuser_set.filter(user=request.user)
        if test_group.exists() or obj.free:
            return True
        return False


class HasTestAccessGroupCategory(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_object_permission(self, request, view, obj):
        test_group = obj.test_group.testgroupuser_set.filter(user=request.user)
        if test_group.exists() or obj.test_group.free:
            return True
        return False
