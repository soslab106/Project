from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.urls import reverse
from .models import Blog, BlogType
from .forms import BlogForm
from read_statistic.utils import read_statistic_once_read

def post_blog(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, user=request.user)
        if blog_form.is_valid():
            blog = Blog()
            blog.author = blog_form.cleaned_data['user']
            blog.title = blog_form.cleaned_data['title']
            blog.content = blog_form.cleaned_data['content']
            blog.blog_type = blog_form.cleaned_data['blog_type']
            blog.save()
            return redirect(f'/blog/{blog.id}')
    else:
        blog_form = BlogForm()
    context = {}
    context['blog_form'] = blog_form
    context['return_back_url'] = redirect_to
    return render(request, 'blog/blog_post.html', context)

def blog_list(request):

    blogs_all_list = Blog.objects.all()

    context= get_blog_list_common_data(request, blogs_all_list)

    return render(request, 'blog/blog_list.html', context) #將字典返回到'bloglist.html'

def blog_detail(request, blog_pk): #導入 blog_pk 變數
    blog = get_object_or_404(Blog, pk=blog_pk)  #獲取blog_pk
    read_cookie_key = read_statistic_once_read(request, blog) #使用閱讀計數
    
    context={}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    response = render(request, 'blog/blog_detail.html', context) #將字典返回到'blog_detail.html'
    response.set_cookie(read_cookie_key, 'true') #閱讀cookie
    return response

def blogs_with_type(request, blog_type_pk): #導入 blog_type_pk 變數

    blog_type = get_object_or_404(BlogType, pk=blog_type_pk) #獲取編號
    blogs_all_list = Blog.objects.filter(blog_type=blog_type) #取得分類後的資料

    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type #將過濾後的資料存入變數

    return render(request, 'blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month): 

    blogs_all_list = Blog.objects.filter(created_time__year = year, created_time__month = month) #篩選取得日期歸檔後的資料    

    context = get_blog_list_common_data(request, blogs_all_list)
    #供面板標題使用(傳送到<blogs_with_date.html>模板頁面)
    context['blogs_with_date'] = '%s年%s月' % (year, month) 

    return render(request, 'blog/blogs_with_date.html', context) #傳送到<blogs_with_date.html>

def get_blog_list_common_data(request, blogs_all_list):

    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) #根據settings自定義參數進行分頁
    page_num = request.GET.get('page', 1) #獲取url的頁面參數 (GET請求)
    page_of_blogs = paginator.get_page(page_num) #get_page會自動識別頁碼，若無效則返回1，超出頁數則顯示最後一頁
    current_page_num = page_of_blogs.number #獲取當前頁碼
    #獲取當前頁碼前後各2頁範圍
        #list 建立串列、range 範圍內的所有值(不包含最後一項，所以尾項要+1)、max 取最大值、min 取最小值、paginator.num_pages 取得總頁數
        #串列(範圍(當前頁數-2，到當前頁數，再跟1相比，小於1則取1)
        #    +範圍(當前頁數，到當前頁數+2，再跟總頁數相比，若大於總頁數則取總頁數)尾項加上1)
    page_range = list(range(max(1, current_page_num - 2), current_page_num)) + \
                 list(range(current_page_num, min(paginator.num_pages, current_page_num + 2) + 1))
    #加上省略頁碼標記
    if page_range[0] -1 >= 2:  #若第0項減1小於等於2
        page_range.insert(0, '...') #則在串列插入省略符號
    if page_range[-1] + 2 <= paginator.num_pages: #若最後一項加2大於等於總頁數
        page_range.append('...') #則在串列最後加上省略符號
    #加上首頁與尾頁
    if page_range[0] != 1: #若串列第0項不為1
        page_range.insert(0, 1) #則在第0項插入1
    if page_range[-1] != paginator.num_pages: #若串列最後一項項不為總頁數
        page_range.append(paginator.num_pages) #則在串列最後加上總頁數

    #獲取日期歸檔與數量
    blog_dates = Blog.objects.dates('created_time','month',order='DESC') #日期歸檔資料
    blog_dates_dict={} #建立字典(鍵(日期歸檔的資料):值(篇數))
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count #迴圈儲存"鍵 = [值]"

    context={} #建立字典
    blog_type_count = BlogType.objects.annotate(blog_count=Count('blog')) #統計BlogType關聯項的Blog模組的小寫
    context['blog_types'] = blog_type_count
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_dates'] = blog_dates_dict
    context['page_range'] = page_range #取得分頁器資訊

    return context