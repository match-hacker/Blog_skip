#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: cyp  date: 2018-10-11

from rest_framework import viewsets
from blog import models
from blog.rest_serializer import UserSerializer, BlogSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = models.Blog.objects.all()
    serializer_class = BlogSerializer
