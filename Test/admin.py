from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import TestGroupCategory, TestGroup, TestCategory, TestTasks, TestGroupUser
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline, TranslationTabularInline


# Register your models here.

class TestTasksInlineAdmin(TranslationStackedInline):
    model = TestTasks

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(TestGroup)
class TestGroupAdmin(ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['category']


@admin.register(TestCategory)
class TestCategoryAdmin(TranslationAdmin):
    search_fields = ['name']

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(TestGroupCategory)
class TestGroupCategoryAdmin(TranslationAdmin):
    autocomplete_fields = ['test_group']
    inlines = [TestTasksInlineAdmin]

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class TestGroupUserInline(admin.StackedInline):
    model = TestGroupUser
