from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_pk>', views.course_detail, name = "course_detail"),
    path('<int:course_pk>/subject', views.course_subject, name = "course_subject"),
    path('<int:course_pk>/subject/<int:subject_pk>', views.course_subject_detail, name = "course_subject_detail"),
    path('<int:course_pk>/post_list', views.post_list, name = "post_list"),
    path('<int:course_pk>/post_list/<int:post_pk>', views.post_list_detail, name = "post_list_detail"),
    path('<int:course_pk>/course_member', views.course_member, name = "course_member")
    #path('submit_homework/', views.submit_homework, name="submit_homework"),
]