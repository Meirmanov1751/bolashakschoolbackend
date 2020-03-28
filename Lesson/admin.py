from django.contrib import admin
from .models import Lesson, SubCategory, LessonMaterial, Category

admin.site.register(LessonMaterial)
admin.site.register(Lesson)
admin.site.register(SubCategory)
admin.site.register(Category)