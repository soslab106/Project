from django.contrib import admin
from .models import Course, Subject, Homework, Grade, Post
# Register your models here.
@admin.register(Course)
class courseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'name', 'start_time', 'end_time', 'teacher')
    
    filter_horizontal = ('students',)

@admin.register(Subject)
class subjectAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'text', 'post_time','dead_time')

@admin.register(Homework)
class homeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'file', 'update_date', 'user')

@admin.register(Grade)
class gradeAdmin(admin.ModelAdmin):
    list_display = ('homework', 'grade', 'date_time')

@admin.register(Post)
class postAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'created_time', 'author')
