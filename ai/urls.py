from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views
from ai import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('multi/', views.TestUploadView.as_view()),
    path('', views.FileView.as_view()),
    path('<int:pk>/', views.FileView.as_view()),
    # path('token/obtain/', GoogleLogin.as_view()),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view()), name='token_refresh'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)