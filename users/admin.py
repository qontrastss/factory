from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):

    model = User

    list_display = ('phone', 'first_name', 'birth_date', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'birth_date')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'birth_date', 'password', 'is_staff', 'is_active')}
         ),
    )
    exclude = ('email', )
    search_fields = ('phone', 'first_name')
    ordering = ('phone',)


admin.site.register(User, CustomUserAdmin)