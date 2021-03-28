from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    # return the whole path to the file
    return "custom/{0}/{2}/".format(instance.user.id, filename)

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file

class FileModel(models.Model):
    file = models.ImageField(upload_to='cycleGAN/' ,blank=False, null=False)
    def __str__(self):
        return self.file

class SocialAccount(models.Model):
    providers = models.CharField(max_length=200, default='google')
    unique_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='social', on_delete=models.CASCADE)

def get_upload_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class CustomModel(models.Model):
    modelname = models.CharField(max_length=200, blank=False, null=False)
    file = models.FileField(upload_to=get_upload_path, blank=False, null=False, verbose_name="模型檔案")
    user = models.ForeignKey(User, related_name='custom', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class CustomFilePathModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    modelname = models.CharField(max_length=200, blank=False, null=False)
    file_path = models.CharField(max_length=100, blank=False, null=False)
    date = models.DateField(auto_now_add=True)
'''
class CustomFolder(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)
'''