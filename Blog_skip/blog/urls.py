#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: cyp  date: 2018-09-20
from blog import views
from django.contrib import admin
from django.urls import path, re_path, include
from blog import views
from django.views.static import serve
from Blog_skip import settings
from rest_framework import routers
from blog.rest_views import UserViewSet, BlogViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', BlogViewSet)


urlpatterns = [
    path('apitest/', views.api_test),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('backend/', views.backend),
    path('add_article/', views.add_article),
    path('add_category/', views.add_category),
    path('poll/', views.poll),
    path('get_comment_tree/(\d+)', views.get_comment_tree),
    path('comment/', views.comment),
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|cate|achrive)/(?P<param>\w+)/$', views.homesite),
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|cate|achrive)/(?P<param>\w+.\d+)/$', views.homesite),
    re_path(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)/$', views.article_detail),
    re_path(r'^(?P<username>\w+)/$', views.homesite),
    path('index/', views.index),

]











