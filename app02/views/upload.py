# 内置
from django.http import HttpResponse
# 第三方
from django.shortcuts import render
from django import forms
# 自定义
from app02.utils.bootstrap import BootstrapForm




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
        context = {

            "form": form
        }
        return render(request, 'upload_form.html', context)

    form = UploadForm(data=request.POST, files=request.FILES)