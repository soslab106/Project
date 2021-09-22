# Generated by Django 3.1 on 2020-10-19 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ai', '0005_auto_20201019_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelname', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='')),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]