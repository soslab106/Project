from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db import models
from .models import *
# Register your models here.
class fileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')
    ordering = ('id',)

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email')
    ordering = ('id', )

class CustomAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'modelname', 'file')
    ordering = ('id', )

class CustomFilePathAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'modelname', 'file_path')
admin.site.register(File, fileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(CustomModel, CustomAdmin)
admin.site.register(CustomFilePathModel, CustomFilePathAdmin)