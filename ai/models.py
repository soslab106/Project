from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file

class FileModel(models.Model):
    file = models.ImageField(upload_to='media/face_recognition/' ,blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file

class SocialAccount(models.Model):
    providers = models.CharField(max_length=200, default='google')
    unique_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='social', on_delete=models.CASCADE)