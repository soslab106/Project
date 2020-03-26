from django.contrib import admin
from django.db import models
from .models import *
# Register your models here.

class NeuralAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'img')
    ordering = ('id',)

class CNNAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'img')
    ordering = ('id',)

admin.site.register(neuralNetwork, NeuralAdmin)
admin.site.register(cnn, CNNAdmin)