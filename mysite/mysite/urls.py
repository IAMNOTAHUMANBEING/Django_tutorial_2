"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from mysite.views import HomeView, UserCreateView, UserCreateDoneTV
from django.conf.urls.static import static  # static 함수는 정적 파일을 처리하기 위해 그에 맞는 url 패턴을 반환하는 함수
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('photo/', include('photo.urls')),
    path('blog/', include('blog.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')), # 장고의 인증 URLconf를 가져와서 사용, /login/, /logout/ 등이 정의되어있고 앞에 붙이고 싶은 건 앞에 쓰면 됨.
    path('accounts/register/', UserCreateView.as_view(), name='register'),
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# settings.MEDIA_URL로 정의된 /media/ URL 요청이 오면 django.views.static.serve() 뷰 함수가 처리하고
# 이 뷰함수에 document_root = settings.MEDIA_ROOT 키워드 인자가 전달됨.
# static.serve() 함수는 개발용이고 상용에는 httpd, nginx 등 웹 서버 프로그램을 사용함.


