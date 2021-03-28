from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Course(models.Model):
    course_id = models.CharField(max_length=10, verbose_name='課程編號')
    name = models.CharField(max_length=20 ,verbose_name='名稱')
    start_time = models.DateField(verbose_name='起始時間')
    end_time = models.DateField(verbose_name='結束時間')
    teacher = models.ForeignKey(User, related_name='course_tacher', on_delete=models.CASCADE, verbose_name='授課教師')
    students = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    title = models.CharField(max_length=30 ,verbose_name='作業標題')
    text = models.TextField(verbose_name='內容')
    post_time = models.DateTimeField(auto_now=True, null=True)
    dead_time = models.DateTimeField(verbose_name='截止時間')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-post_time']

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='作業', null=True)
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, verbose_name='上傳時間')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}|{1}'.format(self.subject, self.user)

class Grade(models.Model):
    grade = models.FloatField(verbose_name='成績')
    homework = models.OneToOneField(Homework, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True, verbose_name='提交時間')

    def __str__(self):
        return str(self.grade)



class Post(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"<Blog: {self.title}>"