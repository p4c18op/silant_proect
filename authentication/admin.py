from django.contrib import admin
from django.contrib.admin import ModelAdmin
from authentication import models, forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    """Регистрация модели CustomUser в админ панели"""

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'email', 'patronymic',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions',),
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )

    list_display = ('model_str', 'email')

    list_filter = ('email', 'first_name', 'last_name',)

    search_fields = ('email', 'first_name', 'last_name',)

    filter_horizontal = ()

    ordering = ('email',)

    add_fieldsets = (
        ("User Details", {'fields': ('username', 'email', 'password1', 'password2',)}),
    )


admin.site.register(models.CustomUser, CustomUserAdmin)
