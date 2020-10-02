from modeltranslation.translator import translator, TranslationOptions
from .models import TestCategory, TestTasks, TestGroupCategory


class TestCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


#
#
class TestGroupTranslationOptions(TranslationOptions):
    fields = ('name',)


class TestTasksTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'ans_a', 'ans_b', 'ans_c', 'ans_d')


#
#
translator.register(TestCategory, TestCategoryTranslationOptions)
translator.register(TestTasks, TestTasksTranslationOptions)
translator.register(TestGroupCategory, TestGroupTranslationOptions)
