from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse
from .models import Course, Subject, Homework, Post
from .forms import HomeworkForm
from blog.models import Blog
from datetime import datetime
# Create your views here.
def course_list(request):
    course_list = Course.objects.filter(students=request.user)
    context = {}
    context['course_list'] = course_list
    return render(request, 'course/course_list.html', context)

def course_detail(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    count = course.students.all().count()
    context = {}
    context['course'] = course
    context['count'] = count
    return render(request, 'course/course_detail.html', context)

def course_subject(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    subjects = Subject.objects.filter(course=course)
    context = {}
    if subjects != None:
        context['subjects'] = subjects
    else:
        context['subjects'] = None
    context['course'] = course
    return render(request, 'course/course_subject.html', context)

def course_subject_detail(request, course_pk, subject_pk):
    course = get_object_or_404(Course, pk=course_pk)
    subject = get_object_or_404(Subject, pk=subject_pk)
    dead_time = subject.dead_time
    date_format = '%Y-%m-%d %H:%M:%S'
    a = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), date_format)
    b = datetime.strptime(dead_time.strftime("%Y-%m-%d %H:%M:%S"), date_format)
    delta = a - b
    day = delta.days
    second = delta.seconds
    date_status = True
    if delta.days > 0:
        date_status = False
    if delta.days == 0 and delta.seconds > 0:
        date_status = False
    context = {}
    context['course'] = course
    context['subject'] = subject
    context['date_status'] = date_status
    return render(request, 'course/course_subject_detail.html', context)

def post_list(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    post_list = Post.objects.filter(course=course)

    context = {}
    if post_list != None:
        context['post_list'] = post_list
    else:
        context['post_list'] = None
    context['course'] = course
    return render(request, 'course/course_post.html', context)

def post_list_detail(request, course_pk, post_pk):
    course = get_object_or_404(Course, pk=course_pk)
    post = get_object_or_404(Post, pk=post_pk)
    context = {}
    context['course'] = course
    context['post'] = post
    return render(request, 'course/course_post_detail.html', context)

def course_member(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    teacher = course.teacher
    students = course.students.all()
    context = {}
    context['course'] = course
    context['students'] = students
    return render(request, 'course/course_member.html', context)