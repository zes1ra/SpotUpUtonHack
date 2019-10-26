from django.contrib import admin
from .models import UserCustom


class UserCustomAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'phone',
        'first_name',
        'last_name',
        'is_staff',
        # 'country',
        # 'city',
        # 'street',
        # 'index',
        # 'info'
    )
    list_filter = ('username',)


admin.site.register(UserCustom, UserCustomAdmin)


# from django.contrib import admin
# #from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import UserCustom
#
#
# class EmployeeInline(admin.StackedInline):
#     model = UserCustom
#     can_delete = False
#     verbose_name_plural = 'custom'
#
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (EmployeeInline,)
#
#
# admin.site.unregister(UserCustom)
# admin.site.register(UserCustom, UserAdmin)
