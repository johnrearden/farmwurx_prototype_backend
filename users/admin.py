from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {
            'fields': (
                'push_notification_token',
                'user_type',
                'main_language',
                'secondary_language',
            )
        }),
    )  
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {
            'fields': (
                'push_notification_token',
                'user_type',
                'main_language',
                'secondary_language',
            )
        }),
    )
    list_display = UserAdmin.list_display + ('user_type', 'main_language', 'secondary_language')
    search_fields = UserAdmin.search_fields + ('user_type', 'main_language', 'secondary_language')
    list_filter = UserAdmin.list_filter + ('user_type', 'main_language', 'secondary_language')
