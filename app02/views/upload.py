# 内置
import os
# 第三方
from django.shortcuts import render
from django import forms
from django.http import HttpResponse

# 自定义
from app02.utils.bootstrap import BootstrapForm
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
        db_file_path = os.path.join("static","img", image_obj.name)

        # file_path = "app02/static/img/{}".format(image_obj.name)
        file_path = os.path.join("app02", db_file_path)

        f = open(file_path, mode='wb')
        for chunk in image_obj.chunks():
            f.write(chunk)
        f.close()

        # 2. 将图片路径写入数据库
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=db_file_path,
        )

    return  render(request, 'upload_form.html', {"form": form})

















