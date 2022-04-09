from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)
from auths.models import CustomUser
from new_app.models import (
    File, 
    Homework,
)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (
            None, {
                'fields': (
                    'email', 'password',
                ),
            }
        ),
        (
            'Permissions', {
                'fields': ('is_active',)
            }
        ),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'email', 'password1', 'password2', 'is_active',
                ),
            }
        ),
    )
    list_display = ('email', 'is_active',)
    list_filter = ('email', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)

class FileAdmin(admin.ModelAdmin):
    readonly_fields=(
        'title_file',
        'file',
    )

class HomeworkAdmin(admin.ModelAdmin):
    readonly_fields=(
        'title_homework',
        'subject',
        'logo',
    )

admin.site.register(
    File, FileAdmin
)

admin.site.register(
    Homework, HomeworkAdmin
)