from modeltranslation.translator import translator, TranslationOptions
from .models import Lesson, LessonTasks, Category


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class LessonTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'vimeo')


class LessonTaskTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'ans_a', 'ans_b', 'ans_c', 'ans_d')


translator.register(Category, CategoryTranslationOptions)
translator.register(Lesson, LessonTranslationOptions)
translator.register(LessonTasks, LessonTaskTranslationOptions)
