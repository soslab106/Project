import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChooseSchoolForm, ChangePasswordForm, ForgotPasswordForm
from .models import Profile
from blog.views import get_blog_list_common_data
from blog.models import Blog
# Create your views here.
    
def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

def register(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #create user
            user = User.objects.create_user(username, email, password)
            user.save()
            #login
            del request.session['register_code']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))

def user_info(request):
    user = request.user
    if user.is_authenticated:
        user_blog_list = Blog.objects.filter(author=user).order_by('-created_time')
        context= get_blog_list_common_data(request, user_blog_list)
        return render(request, 'user/user_info.html', context)

    return render(request, 'user/user_info.html')

def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['warning'] = '若無暱稱則顯示帳戶名稱'
    context['page_title'] = '修改暱稱'
    context['form_title'] = '修改暱稱'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def choose_school(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = ChooseSchoolForm(request.POST, user=request.user)
        if form.is_valid():
            school = form.cleaned_data['school']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.school = school
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChooseSchoolForm()

    context = {}
    context['warning'] = '確認後不能更改，請謹慎選擇'
    context['page_title'] = '選擇學校'
    context['form_title'] = '選擇學校'
    context['submit_text'] = '確認'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '綁定電子信箱'
    context['form_title'] = '綁定電子信箱'
    context['submit_text'] = '綁定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    message = request.GET.get('message', '')
    data = {}

    if email != '':
        # 生成驗證碼
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            
            # 發送郵件
            send_mail(
                f'HowAI Lab - {message}',
                '你的驗證碼是：%s' % code,
                'howailab106@gmail.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密碼'
    context['form_title'] = '修改密碼'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def forgot_password(request):
    redirect_to = reverse('user_login')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密碼'
    context['form_title'] = '重置密碼'
    context['submit_text'] = '確認'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)