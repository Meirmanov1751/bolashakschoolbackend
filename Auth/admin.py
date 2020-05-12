from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, ImportExportMixin, ExportMixin
from import_export.widgets import ForeignKeyWidget

from common.paginator import TimeLimitedPaginator
from .models import MyUser, UserGroups, Analytics, AnalyticsChild, ActivationChange
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class InlineChangeList(object):
    can_show_all = True
    multi_page = True
    get_query_string = ChangeList.__dict__['get_query_string']

    def __init__(self, request, page_num, paginator):
        self.show_all = 'all' in request.GET
        self.page_num = page_num
        self.paginator = paginator
        self.result_count = paginator.count
        self.params = dict(request.GET.items())


class AnalyticsChildTabularAdmin(admin.TabularInline):
    model = AnalyticsChild
    readonly_fields = ('path', 'user', 'admin_link')
    ordering = ('created_date',)
    template = 'admin/edit_inline/list.html'
    per_page = 10
    extra = 0
    can_delete = False

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(AnalyticsChildTabularAdmin, self).get_formset(
            request, obj, **kwargs)

        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)

                qs = self.queryset
                paginator = Paginator(qs, self.per_page)
                try:
                    page_num = int(request.GET.get('page', ['0'])[0])
                except ValueError:
                    page_num = 0

                try:
                    page = paginator.page(page_num + 1)
                except (EmptyPage, InvalidPage):
                    page = paginator.page(paginator.num_pages)

                self.page = page
                self.cl = InlineChangeList(request, page_num, paginator)
                self.paginator = paginator

                if self.cl.show_all:
                    self._queryset = qs
                else:
                    self._queryset = page.object_list

        PaginationFormSet.per_page = self.per_page
        return PaginationFormSet

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                              'myuser'),
                      args=(instance.user.id,))
        return format_html(u'<a href="{}">Посмотреть пользователя</a>', url)


class LimitedAnalyticsChildTabularAdminLimited(admin.TabularInline):
    model = AnalyticsChild
    readonly_fields = ('path', 'user', 'admin_link')
    ordering = ('created_date',)
    max_num = 5

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_changelist' % (instance._meta.app_label,
                                                  'analyticschild'))
        url += '?q=%s' % (instance.user.email)
        return format_html(u'<a href="{}">Посмотреть пользователя</a>', url)


class UserGroupsInline(admin.TabularInline):
    model = UserGroups.users.through


class HistoryGroupsInline(admin.TabularInline):
    model = ActivationChange
    readonly_fields = ['user', 'group_names', 'activation_date']


class UserResource(resources.ModelResource):
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name')


class ActivationResource(resources.ModelResource):
    class Meta:
        model = ActivationChange
        fields = ('user__email', 'user__first_name', 'user__last_name', 'activation_date', 'group_names')

class ActivationAdmin(ImportExportModelAdmin):
    resource_class = ActivationResource

class UserAdmin(ExportMixin, BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    resource_class = UserResource
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'first_name', 'last_name', 'is_active', 'created', 'modified')
    list_filter = ('is_admin', 'type', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'fathers_name', 'phone')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_verified', 'active_until')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ('email',)
    filter_horizontal = ()
    inlines = [UserGroupsInline, HistoryGroupsInline]


class UserGroupsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'sub_category__name']
    filter_horizontal = ('users', 'sub_category')


class AnalyticsChildAdmin(admin.ModelAdmin):
    paginator = TimeLimitedPaginator
    search_fields = ('user__first_name', 'user__email', 'analytics__created_date')
    list_display = ('user', 'created_date')


class AnalyticsAdmin(admin.ModelAdmin):
    paginator = TimeLimitedPaginator
    inlines = [AnalyticsChildTabularAdmin, ]
    search_fields = ('created_date',)


admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(AnalyticsChild, AnalyticsChildAdmin)
# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(UserGroups, UserGroupsAdmin)
admin.site.register(ActivationChange, ActivationAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.site_header = "Yessenov online"
admin.site.site_title = "Yessenov online Admin Portal"
admin.site.index_title = "Welcome to Yessenov online Administration"
