from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import School, Profile
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('id', 'username', 'nickname', 'school', 'email', 'is_staff', 'is_superuser', 'last_login')

    def nickname(self, obj):
        return obj.profile.nickname
    def school(self, obj):
        return obj.profile.school

    nickname.short_description = '暱稱'
    school.short_description = '學校'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'school')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('title',)