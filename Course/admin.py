from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Course, LessonTasks, Module, Lesson, Category, ModuleUser, ModulePrice
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline, TranslationTabularInline


# Register your models here.
class LessonTasksTabularAdmin(TranslationStackedInline):
    model = LessonTasks
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(LessonTasks)
class LessonTaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['module']


@admin.register(Lesson)
class LessonAdmin(TranslationAdmin):
    inlines = [LessonTasksTabularAdmin]
    autocomplete_fields = ['category']
    list_display = ['name', 'category']
    search_fields = ['name', 'category__name']
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['course']
    search_fields = ['name']


class ModuleUserInline(admin.StackedInline):
    model = ModuleUser
