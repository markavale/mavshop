from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'ip_address', 'is_superuser', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (  # For Updating fields on Admin Panel
        (('Additional Personal Info'), {'fields': ('image','ip_address',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (  # For Creating User on Admin Panel
        (('Personal Info'), {'fields': ('email','image','ip_address',)}),
    )


admin.site.register(User, UserAdmin)