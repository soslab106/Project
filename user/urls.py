from django.urls import path
from . import views

urlpatterns = [
    path('user_login/', views.login, name='user_login'),
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),
    path('register/', views.register, name='register'),
    path('user_logout/', views.logout, name='user_logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('choose_school/', views.choose_school, name='choose_school'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]