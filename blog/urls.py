from django.urls import path
from . import views

urlpatterns = [
    path('',views.blog_list, name='blog_list'), #將原先的部落格頁面路徑修改至此
    #連接文章標題至文章詳細頁面
    path('<int:blog_pk>', views.blog_detail, name = "blog_detail"),
    #連接文章份類至分類頁面
    path('type/<int:blog_type_pk>', views.blogs_with_type, name = "blogs_with_type"),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name = "blogs_with_date"),
    path('post_blog/', views.post_blog, name="post_blog"),

]