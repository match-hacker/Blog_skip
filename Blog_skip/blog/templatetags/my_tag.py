#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: cyp  date: 2018-09-22

from django.db.models import Count
from blog.models import *
from django import template
register = template.Library()

@register.simple_tag
def mul(x,y):
    return x*y
# 让乘法脚本在模板里可以调用，要加真石漆,,@register.filter是过滤器，，@register.simple_tag是一个标签


@register.inclusion_tag("menu.html")
def get_menu(username):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    cate_list = Category.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
    tag_list = Tag.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
    # 按日期分类
    date_list = Article.objects.filter(user=user).extra(
        select={"create_ym": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values("create_ym").annotate(
        c=Count("nid")).values_list("create_ym", "c")
    return {"username": username, "cate_list": cate_list, "tag_list": tag_list, "date_list": date_list}






















