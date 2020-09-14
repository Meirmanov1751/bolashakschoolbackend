from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Course, LessonTasks, Module, Lesson, Category, ModuleUser, ModulePrice
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline, TranslationTabularInline


# Register your models here.
class LessonTasksTabularAdmin(TranslationTabularInline):
    model = LessonTasks
    fields = ['name', 'change_link']
    readonly_fields = ['name', 'change_link']
    # classes = ['collapse']
    show_change_link = True
    def change_link(self, obj):
        return mark_safe('<a href="%s" class="button">Изменить</a>' % \
                         reverse('admin:Course_lessontasks_change',
                                 args=(obj.id,)))
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


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['course']
    search_fields = ['name']


class ModuleUserInline(admin.StackedInline):
    model = ModuleUser
