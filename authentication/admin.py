from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
