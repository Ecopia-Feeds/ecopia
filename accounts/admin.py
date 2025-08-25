from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, AuditLog

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'phone','full_name', 'role_choice', 'is_active', 'is_staff')
    list_filter = ('role_choice', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'role_choice')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'expiry_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role_choice', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(Profile)
admin.site.register(AuditLog)
