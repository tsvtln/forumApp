from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .forms import CustomUserChangeForm, CustomUserForm
from .models import AppUser, Profile

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserForm
    list_display = ('username', 'email')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    fieldsets = (
        ('Credentials', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)})
    )

#
# @admin.register(UserModel)
# class UserAdmin(UserAdmin):
#     list_display = ('username', 'email')
#
#     fieldsets = (
#         ('Credentials', {'fields': ('email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login',)})
#     )

#
# # Register your models here.
# @admin.register(AppUser)
# class AppUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
#     fieldsets = UserAdmin.fieldsets
#     add_fieldsets = UserAdmin.add_fieldsets
#
#
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'first_name', 'last_name', 'age', 'points')
