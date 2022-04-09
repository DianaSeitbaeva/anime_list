from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.contrib import admin
from django.forms import ValidationError

from auths.models import CustomUser
from .models import (
    # Account, 
    Group, 
    Student, 
    Professor
)

from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    readonly_fields = ()

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[CustomUser] = None
    ) -> tuple:
        if not obj:
            return self.readonly_fields

        return self.readonly_fields + (
            'first_name',
            'last_name',
            'email',
            'username',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
        )


# admin.site.register(
#     CustomUser, CustomUserAdmin
# )



# class AccountAdmin(admin.ModelAdmin):
#     readonly_fields = (
#         'datetime_created',
#         'datetime_updated',
#         'datetime_deleted'
#     )

#     def get_readonly_fields(
#         self,
#         request: WSGIRequest,
#         obj: Optional[Account] = None
#     ) -> tuple:
#         if obj:
#             return self.readonly_fields + ('description',)
#         return self.readonly_fields

class GroupAdmin(admin.ModelAdmin):
    readonly_fields = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted'
    )

    # def get_readonly_fields(
    #     self,
    #     request: WSGIRequest,
    #     obj: Optional[Group] = None
    # ) -> tuple:
    #     if obj:
    #         return self.readonly_fields + ('name',)
    #     return self.readonly_fields

class StudentAdmin(admin.ModelAdmin):
    readonly_fields = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted'
    )
    # list_filter = (
    #     'age',
    #     'gpa',
    # )
    # search_field = (
    #     'account__full_name',
    # )
    # list_display = (
    #     'account__full_name',
    #     'age',
    #     'gpa',
    # )

    MAX_STUDENT_AGE = 16

    def student_age_validation(
        self,
        obj:Optional[Student]
    ) -> tuple:
        if obj and obj.age <= self.MAX_STUDENT_AGE:
            return self.readonly_fields + ('age',)
        return self.readonly_fields

    def student_age_validation_2(
        self,
        obj: Optional[Student]
    ) -> bool:
        if obj and obj.age <= self.MAX_STUDENT_AGE:
            return True
        return False

        #Подкапотный движ:
        #return a.k.a return None

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Student] = None
    ) -> tuple:
    
        result: tuple = self.student_age_validation(obj)
        return result

        #result: bool = self.student_age_validation_2(obj)
        #if result:
            #return self.readonly_fields + ('age',)
        #return self.readonly_fields


class ProfessorAdmin(admin.ModelAdmin):
    readonly_fields = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted'
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Professor] = None
    ) -> tuple:
        if obj:
            return self.readonly_fields + ('full_name',)
        return self.readonly_fields
        

# admin.site.register(
#     Account, AccountAdmin
# )

admin.site.register(
    Group, GroupAdmin
)

admin.site.register(
    Student, StudentAdmin 
)

admin.site.register(
    Professor, ProfessorAdmin 
)