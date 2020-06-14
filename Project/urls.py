"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ai.views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

# from imgnet.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('yolo/', renderYolo),
    path('postCnnModels/', postCnnModels),
    # path('postImgNet/', postImgNet),
    path('', renderIndex),
    path('VGG16/', renderVgg),
    path('resNet101/', renderResNet),
    path('facenet/', renderFacenet),
    # path('faceRecog/', face_recog_test),
    # path('face_recog_test/', face_recog_test),
    # path('test/', renderTest),
    path('upload/', include('ai.urls')),
    path('login/', LoginPage.as_view(), name='login'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.social.urls')),
    path('googleLogin/', include('ai.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
