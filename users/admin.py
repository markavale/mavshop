from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'first_name',
                    'last_name', 'gender', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (  # For Updating fields on Admin Panel
        (('Additional Personal Info'), {'fields': ('gender','image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (  # For Creating User on Admin Panel
        (('Personal Info'), {'fields': ('last_name', 'first_name', 'email', 'gender','image',)}),
    )


admin.site.register(User, UserAdmin)