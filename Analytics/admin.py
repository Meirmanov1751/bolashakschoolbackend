from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Analytics, AnalyticsCategory, AnalyticsLesson

class AnalyticsCategoryTaburlarInline(admin.TabularInline):
    model = AnalyticsCategory

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                              instance._meta.model_name),
                      args=(instance.id,))
        # return format_html(u'<a href="{}">Edit</a>', url)
        # … or if you want to include other fields:
        return format_html(u'<a href="{}">Edit: {}</a>', url, instance.name)

    readonly_fields = ('admin_link',)

class AnalyticsAdmin(admin.ModelAdmin):
    model = Analytics
    inlines = [AnalyticsCategoryTaburlarInline]
class AnalyticsCategoryAdmin(admin.ModelAdmin):
    model = AnalyticsCategory

# admin.site.register(AnalyticsCategory, AnalyticsCategoryAdmin)
# admin.site.register(Analytics, AnalyticsAdmin)
# admin.site.register(AnalyticsLesson)