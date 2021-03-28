from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) #透過外鍵指向模型
    object_id = models.PositiveIntegerField() #紀錄對應模型的主鍵值
    content_object = GenericForeignKey('content_type', 'object_id') #集合前兩項成一個通用外鍵
    
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
        