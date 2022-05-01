from django.contrib import admin, messages
from .models import Containers, Instances, DefaultUser, AccessGroup, App, UsersFromCSV
from django.contrib.auth.admin import UserAdmin, Group
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomAppForm, UsersFromCSVForm
from django.urls import path
from django.shortcuts import redirect, reverse


admin.site.site_header = 'System Administration'


@admin.register(DefaultUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'is_staff', 'role', 'group', 'apps_available'
        )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('ROLE info'), {'fields': ('role', 'group')}),
        (_('Personal info'), {'fields': ('email', 'first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'group'),
        }),

    add_form = CustomUserCreationForm

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('add_from_csv/', UsersFromCSVAdmin(UsersFromCSV, admin_site=admin.site).add_view,
                         name='add_from_csv')]
        return new_urls + urls

    list_filter = ('is_staff', 'role', 'group')


class UsersFromCSVAdmin(admin.ModelAdmin):
    form = UsersFromCSVForm
    add_form = UsersFromCSVForm

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def response_add(self, request, obj, post_url_continue=None):
        messages.success(request, 'Users created !')
        return redirect(reverse("admin:main_defaultuser_changelist"))


class AccessGroupAdmin(admin.ModelAdmin):
    list_display = (
        'group',
        'has_access_to',
    )


class AppAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'groups',
    )
    form = CustomAppForm


# admin.site.register(Containers)
# admin.site.register(Instances)
admin.site.register(UsersFromCSV, UsersFromCSVAdmin)
admin.site.register(AccessGroup, AccessGroupAdmin)
admin.site.register(App, AppAdmin)
admin.site.unregister(Group)
# Register your models here.
