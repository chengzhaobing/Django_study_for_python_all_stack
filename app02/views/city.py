# 内置

# 第三方
from django.shortcuts import render,redirect
# 自定义
from app02.utils.bootstrap import BootstrapForm, BootStrapModelForm
from app02 import models

def city_list(request):
    """ ModelForm 上传的数据进行展示 """
    queryset = models.City.objects.all()
    return render(request, 'city_list.html',{"queryset": queryset})

class UploadModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img'] # 定义img字段不使用bootstrap样式
    class Meta:
        model = models.City
        fields = "__all__"
def city_add(request):
    """ 新建展示数据 """

    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UploadModelForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于上传的文件，数据定义的 upload_to方法会自动保存到对应的文件夹
        # 字段 + 上传路径写入到数据库
        form.save()
        return redirect('/city/list/')
    return render(request, 'upload_form.html', {"form": form})