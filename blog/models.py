from django.db import models
from django.contrib.auth.models import User #導入內建的使用者模組
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistic.models import ReadNumExpandMethod, ReadDetail #導入閱讀計數應用的模組
# Create your models here.

class BlogType(models.Model): #部落格文章類型
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model, ReadNumExpandMethod): #部落格文章(由於會用外鍵連接到部落格文章類型，所以此模型要放在後面)
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE) #使用外鍵連接到使用者模組，由於刪除時則會將關聯的對象一併刪除
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add = True)
    last_updated_time = models.DateTimeField(auto_now = True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)  #使用外鍵連接到部落格文章類型

    def __str__(self):
        return f"<Blog: {self.title}>"

    class Meta:
        ordering = ['-created_time']