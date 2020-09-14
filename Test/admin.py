from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import TestGroupCategory, TestGroup, TestCategory, TestTasks, TestGroupUser


# Register your models here.

class TestTasksInlineAdmin(StackedInline):
    model = TestTasks


@admin.register(TestGroup)
class TestGroupAdmin(ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['category']


@admin.register(TestCategory)
class TestCategoryAdmin(ModelAdmin):
    search_fields = ['name']


@admin.register(TestGroupCategory)
class TestGroupCategoryAdmin(ModelAdmin):
    autocomplete_fields = ['test_group']
    inlines = [TestTasksInlineAdmin]


class TestGroupUserInline(admin.StackedInline):
    model = TestGroupUser
