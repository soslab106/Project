from django.db import models

# Create your models here.

class neuralNetwork(models.Model):
    content = models.TextField()
    img = models.ImageField(null=True, blank=True)

class cnn(models.Model):
    content = models.TextField()
    img = models.ImageField(null=True, blank=True)