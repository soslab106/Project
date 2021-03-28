from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class School(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, null=True, verbose_name='暱稱')
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, verbose_name='學校')

    def __str__(self):
        return f'<Profile: {self.nickname} for {self.user.username}>'

def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''

def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username

def has_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        if profile.nickname is not None:
            return True
        else:
            return False
    else:
        return False

def get_school(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.school
    else:
        return ''

def has_school(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        if profile.school is not None:
            return True
        else:
            return False
    else:
        return False

User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
User.has_nickname = has_nickname
User.get_school = get_school
User.has_school = has_school