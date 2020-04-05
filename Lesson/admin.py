from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Lesson, SubCategory, LessonMaterial, Category, UserLesson, Homework


class UserLessonAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    filter_horizontal = ('sub_category', 'homework')


class LessonInlineAdmin(admin.TabularInline):
    model = Lesson

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                              instance._meta.model_name),
                      args=(instance.id,))
        # return format_html(u'<a href="{}">Edit</a>', url)
        # … or if you want to include other fields:
        return format_html(u'<a href="{}">Edit: {}</a>', url, instance.name)

    readonly_fields = ('admin_link',)


class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [LessonInlineAdmin]


class SubCategoryInlineAdmin(admin.TabularInline):
    model = SubCategory

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                              instance._meta.model_name),
                      args=(instance.id,))
        # return format_html(u'<a href="{}">Edit</a>', url)
        # … or if you want to include other fields:
        return format_html(u'<a href="{}">Edit: {}</a>', url, instance.name)

    readonly_fields = ('admin_link',)


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInlineAdmin, ]


admin.site.register(LessonMaterial)
admin.site.register(Lesson)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserLesson, UserLessonAdmin)
admin.site.register(Homework)
