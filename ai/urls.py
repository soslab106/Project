from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ai import views

urlpatterns = [
    path('', views.FileView.as_view()),
    path('<int:pk>/', views.FileView.as_view()),
]