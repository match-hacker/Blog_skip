#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: cyp  date: 2018-10-11

from blog import models
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):HyperlinkedModelSerializer是超链接，ModelSerializer是id
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        depth = 2  # 表示深层展示，2就是2层，3就是三层
        fields = ('url', 'username', 'email', 'telephone', 'create_time', 'avatar', 'blog')


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = ('title', 'site', 'theme')
