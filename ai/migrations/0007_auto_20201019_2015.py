# Generated by Django 3.1 on 2020-10-19 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0006_custommodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custommodel',
            name='file',
            field=models.FileField(upload_to='', verbose_name='模型檔案'),
        ),
    ]