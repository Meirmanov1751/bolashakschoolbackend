from django.contrib import admin
from .models import Lesson, SubCategory, LessonMaterial, Category, UserLesson, Homework


class UserLessonAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    filter_horizontal = ('sub_category', 'homework')


admin.site.register(LessonMaterial)
admin.site.register(Lesson)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(UserLesson, UserLessonAdmin)
admin.site.register(Homework)
