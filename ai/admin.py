from django.contrib import admin
from django.db import models
from .models import *
# Register your models here.
class fileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')
    ordering = ('id',)


admin.site.register(File, fileAdmin)