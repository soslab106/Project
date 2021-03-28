from django.db import models
from django.db.models.fields import exceptions #導入例外處理
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)#透過外鍵指向模型
    object_id = models.PositiveIntegerField() #紀錄對應模型的主鍵值
    content_object = GenericForeignKey('content_type', 'object_id') #集合前兩項成一個通用外鍵

class ReadNumExpandMethod():  #創建擴展用的類別
    def get_read_num(self): #讓被導入的模組，取得關聯的項目編號，若不存在則返回0
        try:
            ct = ContentType.objects.get_for_model(self) #獲取模型內容並存入變數
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk) 
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)#透過外鍵指向模型
    object_id = models.PositiveIntegerField() #紀錄對應模型的主鍵值
    content_object = GenericForeignKey('content_type', 'object_id') #集合前兩項成一個通用外鍵