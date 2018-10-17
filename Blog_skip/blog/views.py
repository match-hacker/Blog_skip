from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from django.http import JsonResponse
import json
import os
from django.contrib import auth
from blog.forms import *
from blog.models import *
from django.db.models import F
from django.db import transaction  # 导入事务
from django.db.models import Count
from Blog_skip import settings
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from blog import rest_serializer


# Create your views here.

def api_test(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data'))
        print(data)
        serializer_obj = rest_serializer.UserSerializer(data=data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            serializer_obj

    return render(request, 'api-test.html', locals())


def login(request):
    if request.is_ajax():
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")
        res = {"state": False, "msg": None}
        valid_str = request.session.get('valid_str')
        if valid_code.upper() == valid_str.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                res['state'] = True
                auth.login(request, user)
                # request.session.set_expiry(60*60)
            else:
                res["msg"] = "userinfo or pwd error"
        else:
            res["msg"] = "验证码错误"
        return JsonResponse(res)

    return render(request, 'login.html')


def get_valid_img(request):
    """验证码"""
    from PIL import Image
    from PIL import ImageDraw, ImageFont  # 创建画笔
    import random

    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    image = Image.new("RGB", (250, 40), get_random_color())
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("blog/static/dist/fonts/ITCBLKAD.TTF", 38)
    temp = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low = chr(random.randint(97, 122))
        random_upper = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low, random_upper])
        draw.text((24 + i * 36, 0), random_char, get_random_color(), font=font)
        temp.append(random_char)
    # 噪点噪线
    width = 250
    height = 40
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    for i in range(20):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    # f = open("valid_code.png", 'wb')
    # image.save(f, "png")
    # f = open("valid_code.png", "rb")
    # data = f.read()
    # f.close()打开了两次，使用的是磁盘句柄（文件句柄，接下来用内存句柄）
    valid_str = "".join(temp)
    print("验证码", valid_str)
    from io import BytesIO
    f = BytesIO()
    image.save(f, "png")
    data = f.getvalue()
    f.close()
    request.session["valid_str"] = valid_str
    return HttpResponse(data)


def reg(request):
    """注册"""
    if request.method == 'POST':
        res = {"user": None, "error_dict": None}
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar = request.FILES.get("avatar")
            if avatar:
                # UserInfo.objects.create(), userinfo及继承了auth，要用下面的方法创建
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email, avatar=avatar)
            else:
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email)
            print(user)
            print(user.username)
            res["user"] = user.username
        else:
            res["error_dict"] = form.errors
        return JsonResponse(res)
    else:
        form = RegForm()
        return render(request, "reg.html", locals())


def index(request):
    article_list = Article.objects.all()
    return render(request, "index.html", {"article_list": article_list})


def homesite(request, username, **kwargs):
    """主页"""
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse('404')
    blog = user.blog
    if not kwargs:
        article_list = Article.objects.filter(user=user)
    else:
        condition = kwargs.get("condition")
        param = kwargs.get("param")
        if condition == "cate":
            article_list = Article.objects.filter(user=user).filter(category__title=param)
        elif condition == "tag":
            article_list = Article.objects.filter(user=user).filter(tags__title=param)
        else:
            year, month = param.split("-")
            print(year,month)
            article_list = Article.objects.filter(user=user).filter(create_time__year=year)
            print(article_list)
            # 查询每一个分类
            # cate_list = Category.objects.filter(blog=blog)
            # 查询每一个分类，和对应的文章数
    # cate_list = Category.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
    # tag_list = Tag.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
    # # 按日期分类
    # date_list = Article.objects.filter(user=user).extra(
    #     select={"create_ym": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values("create_ym").annotate(
    #     c=Count("nid")).values_list("create_ym", "c")
    # ret = Article.objects.filter(user=user).extra(select={"create_ym": "DATE_FORMAT(create_time,'%%Y-%%m')"})
    # .values("title", "create_ym", "create_time")
    return render(request, 'homesite.html', locals())


def article_detail(request, username, article_id):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    article = Article.objects.filter(pk=article_id).first()
    comment_list = Comment.objects.filter(article_id=article_id)
    return render(request, "article_detail.html", locals())


def poll(request):
    print(request.POST)
    # ajax传过来的是字符串“true”或“false”，通过json反序列化成布尔值
    is_up = json.loads(request.POST.get("is_up"))
    article_id = request.POST.get("article_id")
    user_id = request.user.pk
    res={"state": True}
    try:
        with transaction.atomic():
            ArticleUpDown.objects.create(is_up=is_up, article_id=article_id, user_id=user_id)
            if is_up:  # 如果是赞就赞加1
                Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
            else:  # 如果是灭就灭加1
                Article.objects.filter(pk=article_id).update(down_count=F("down_count")+1)
    except Exception as e:
        res["state"] = False
        res["first_action"] = ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first().is_up

    return JsonResponse(res)


def comment(request):
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    pid = request.POST.get("pid")
    user_id = request.user.pk
    res={"state": True}
    with transaction.atomic():  # 数据库事务管理
        if not pid:  # 提交根评论
                obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content)
        else:
                obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content, parent_comment_id=pid)
        Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)
    res["time"] = obj.create_time.strftime("%Y-%m-%d %H:%M")  # json不能序列化时间对象，但是jsonresponse可以，保险起见用str处理
    res["content"] = obj.content
    return JsonResponse(res)


def get_comment_tree(request, id):
    ret = list(Comment.objects.filter(article_id=id).values("pk", "content", "parent_comment_id", "user__username"))
    return JsonResponse(ret, safe=False)  # JsonResponse一直序列化字典，序列化列表需要加safe=False


@login_required
def backend(request):
    return render(request, "backend.html")


@login_required
def add_article(request):
    user = request.user.username
    nid = UserInfo.objects.filter(username=user).values("blog_id")[0]['blog_id']
    if nid:
        pk = request.user.pk
        fl = request.POST.get("fl")
        print("ddddd", fl)
        blog_id = UserInfo.objects.filter(nid=pk).values_list("blog_id")[0][0]
        # print(blog_id)
        category = Category.objects.filter(blog_id=blog_id).values("title", "nid")
        print(category)
        if request.method == "POST":
            title = request.POST.get("title")
            article_con = request.POST.get("article_con")
            soup = BeautifulSoup(article_con, "html.parser")
            for tag in soup:
                if tag.name == "script":
                    tag.decompose()
            article_obj = Article.objects.create(title=title, user=request.user, desc=soup.text[0: 150], category_id=fl)
            ArticleDetail.objects.create(content=soup.prettify(), article=article_obj)
            return render(request, "success.html")

        return render(request, "add_article.html", locals())
    return HttpResponseRedirect("/create_blog/")


def upload_img(request):
    print(request.FILES)
    img_obj = request.FILES.get('img')
    media_path = settings.MEDIA_ROOT
    path = os.path.join(media_path, "article_imgs", img_obj.name)
    f = open(path, "wb")
    for line in img_obj:
        f.write(line)
    f.close()
    res = {"url": "/media/article_imgs/" + img_obj.name,
           "error": 0}

    return HttpResponse(json.dumps(res))


@login_required
def upload_file(request):
    user = request.user.username
    nid = UserInfo.objects.filter(username=user).values("blog_id")[0]['blog_id']
    if nid:
        if request.method == 'POST':
            obj = request.FILES.get('css')
            theme_path = settings.THEME_ROOT
            path = os.path.join(theme_path, "theme", obj.name)
            f = open(path, "wb")
            for line in obj:
                f.write(line)
            f.close()
            return HttpResponse("上传成功")
        else:
            return render(request, 'add_css.html')
    return HttpResponseRedirect("/create_blog/")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


def change(request):
    # raise Http404("url %s/%s not found")
    return render(request, "404.html")



def change_pwd(request):
    return render(request, "recharge.html")


@login_required
def create_blog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        suffix = request.POST.get("suffix")
        theme = request.POST.get("theme")
        username = request.user.username
        bbl = UserInfo.objects.filter(username=username).values("blog")[0]['blog']
        if not bbl:
            try:
                blog = Blog.objects.create(title=title, site=suffix, theme=theme)
                UserInfo.objects.filter(username=username).update(blog=blog)
            except Exception as e:
                return HttpResponseRedirect("/change_pwd/")
            else:
                return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/change_pwd/")
    return render(request, 'create_blog.html')


@login_required
def add_category(request):
    pk = request.user.pk
    blog_id = UserInfo.objects.filter(nid=pk).values_list("blog_id")[0][0]
    print(blog_id)
    category = request.POST.get("category")
    Category.objects.create(title=category, blog_id=blog_id)
    return HttpResponseRedirect("/blog/add_article/")




