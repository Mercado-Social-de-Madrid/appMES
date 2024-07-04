from django.contrib import admin
from django import forms
from django.contrib.admin import ModelAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from authentication.models import User

from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authentication.models.api_token import APIToken
from authentication.models.group import Group
from rest_framework.authtoken.models import TokenProxy as DRFToken
from rest_framework.authtoken.admin import TokenAdmin as DRFTokenAdmin

from authentication.models.preregister import PreRegisteredUser

admin.site.unregister(DjangoGroup)
admin.site.unregister(DRFToken)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label=_("Contraseña"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Repetir contraseña"), widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
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
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField(
        label=_('Contraseña'),
        help_text=_('Puedes cambiar la contraseña haciendo click en <a href="../password/">este enlace</a>.'),
        required=False)

    class Meta:
        model = User
        fields = ["email", "password", "is_active", "is_staff", "preferred_locale"]


class UserPasswordChangeForm(AdminPasswordChangeForm):
    """Customizing the admin password change form to include additional fields."""

    class Meta:
        model = User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = UserPasswordChangeForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ('created_at', 'updated_at', )
    filter_horizontal = ('groups', 'user_permissions')
    ordering = ['email']
    fieldsets = (
        (_('Información'), {
            'fields': ('email', 'first_name', 'last_name', 'password', 'preferred_locale'),
        }),
        (_('Fechas'), {
            'fields': ('date_joined', 'last_login', 'created_at', 'updated_at',),
        }),
        (_('Permisos'), {
            'fields': ('groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active')
        }),
    )
    add_fieldsets = [
        (None, {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name", "password1", "password2"],
        }),
    ]


@admin.register(PreRegisteredUser)
class PreRegisteredUserAdmin(ModelAdmin):
    pass


@admin.register(APIToken)
class TokenAdmin(DRFTokenAdmin):
    pass
