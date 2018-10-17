"""Blog_skip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path, include
from blog import views
from django.views.static import serve
from Blog_skip import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('logout/', views.logout),
    path('get_valid_img/', views.get_valid_img),
    path('index/', views.index),
    path('', views.index),
    path('reg/', views.reg),
    path('blog/', include("blog.urls")),
    path('upload_img/', views.upload_img),
    path('add_css/', views.upload_file),
    path('create_blog/', views.create_blog),
    path('change/', views.change),
    path('change_pwd/', views.change_pwd),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
# re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
# 这个是为了把media的接口打开，还有settings，
# MEDIA_ROOT = os.path.join(BASE_DIR, 'blog', 'media')
# MEDIA_URL = "/media/"