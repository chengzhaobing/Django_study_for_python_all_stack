# 内置
import os
# 第三方
from django.shortcuts import render,redirect
from django import forms
from django.http import HttpResponse

# 自定义
from app02.utils.bootstrap import BootstrapForm, BootStrapModelForm
from app02 import models



def upload_list(request):
    """ 文件上传 """
    if request.method == "GET":
        return render(request,"upload_list.html")

    # print(request.POST) # 请求体中的数据
    # print(request.FILES) # 请求发过来的文件

    file_obj = request.FILES["upload_file"] # upload_file 为上传文件的input框
    print(file_obj.name) # 取文件名

    # f =open(file_obj.name, "wb") # file_obj.name 指使用上传的源文件名
    f = open('f1.png', mode='wb') # 分块写入的位置（未指定：根目录）/写入的名称 --- 默认文件根目录
    for chunk in file_obj.chunks(): # 文件对象分块
        f.write(chunk) # 分块写入
    f.close() #写入完成关闭

    return HttpResponse("ok")



class UploadForm(BootstrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")

def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UploadForm()
        return render(request, 'upload_form.html', {"form": form})

    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # print(form.cleaned_data)
        # {'name': '田曦薇', 'age': 22, 'img': < InMemoryUploadedFile: f1.png(image / png) >}
        # 1. 读取图片内容， 写入到文件夹中并获取文件路径。
        image_obj = form.cleaned_data.get("img")

        # 数据库存储路径  1 | 田曦薇 |  23 | app02\static\img\f1.png
        # 浏览器访问路径：http://127.0.0.1:8000/static/img/f1.png
        # 因为浏览器的实际访问路径会多一个app02的路径，所有这里重新拼接

        # 使用settings.py下配置好的media目录
        from django.conf import settings
        # db_file_path = os.path.join("static","img", image_obj.name)
        # media文件夹绝对路径  E:\PycharmProjects\dya2\media\f3.png
        media_path = os.path.join(settings.MEDIA_ROOT, image_obj.name)
        # media文件夹相对路径  media\f4.png
        media_path = os.path.join("media", image_obj.name)
        # 为什么要绝对路径，因为可以通过已经存在的网站网址进行拼接访问到数据库存储的照片
        # eg：http://127.0.0.1:8000/static/img/f1.png

        # file_path = "app02/static/img/{}".format(image_obj.name)
        # file_path = os.path.join("app02", db_file_path)






        f = open(media_path, mode='wb')
        # f = open(file_path, mode='wb')
        for chunk in image_obj.chunks():
            f.write(chunk)
        f.close()

        # 2. 将图片路径写入数据库
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            # img=db_file_path,
            img=media_path,
        )

    return  render(request, 'upload_form.html', {"form": form})



class UploadModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img'] # 定义img字段不使用bootstrap样式
    class Meta:
        model = models.City
        fields = "__all__"



def upload_modelform(request):
    """ modelform上传 """
    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UploadModelForm()
        return render(request, 'upload_form.html', {"form": form,"title":title})

    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于上传的文件，数据定义的 upload_to方法会自动保存到对应的文件夹
        # 字段 + 上传路径写入到数据库
        form.save()
        return redirect('/city/list/')
    return render(request, 'upload_form.html', {"form": form})










