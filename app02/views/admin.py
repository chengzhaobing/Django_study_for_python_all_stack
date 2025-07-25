# 内置模块
from django import forms
from django.core.exceptions import ValidationError
#第三方模块
from django.shortcuts import render, redirect

# 自定义模块
from app02 import models
from app02.utils.bootstrap import BootStrapModelForm
from app02.utils.pagination import Pagination
from app02.utils.encrypt import md5
def admin_list(request):
    """ 管理员列表 """
    # info = request.session['info'] # 把获取当前的登录信息
    # print(info)


    # 检查用户是否登录，已登录，继续向下走。未登录，跳转到登录页面（没有登录不让访问其他的网址）
    # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看Session表中是否存在该用户
    #                                 写入 Session_data 的数据
    # request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}

    # info = request.session.get('info') #  获取 Session_data 的数据
    # if not info:
    #     return redirect('/login/')

    # print(info)
    # {'id': 7, 'name': 'cheng'} -----有cookie状态能获取到 Session_data
    # [22/Jul/2025 16:04:52] "GET /admin/list/ HTTP/1.1" 200 8372
    # None                       -----无cookie状态None
    # [22/Jul/2025 16:05:14] "GET /admin/list/ HTTP/1.1" 200 8372




    # 构造搜索
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        # data_dict = {"name__contains":value}
        data_dict["username__contains"] = search_data

    # 根据条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)
    # 分页
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_data": search_data,
    }

    return render(request, 'admin_list.html', context)

class AdminModelForm(BootStrapModelForm):
    # 确认密码字段
    confirm_password = forms.CharField(
        label="确认密码",
        # 定义confirm_password字段密码框，使其不再是明文输入，而是密文
        # render_value=True表示两次输入密码不一致，不清空重新输入，反之清空
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        # 定义password字段为密码框，使其不再是明文输入，而是密文
        # render_value=True表示两次输入密码不一致，不清空重新输入，反之清空
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    # 钩子函数——数据密码字段md5加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 钩子函数 clean_字段名():
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入！")
        # 返回的是保存到数据库的数据
        return confirm

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]

class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.Admin
        fields = ["password","confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 修改密码提示不能与上一次密码一致
        md5_pwd = md5(pwd)
        # 去数据库校验，当前密码和数据库密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同!")
        return md5(pwd)

    # 钩子函数 clean_字段名():
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入！")
        # 返回的是保存到数据库的数据
        return confirm


def admin_add(request):
    """ 新建管理员 """
    title = "添加管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {"form":form,"title":title})

    form = AdminModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {"form":form,"title":title})

def admin_edit(request, nid):
    """ 编辑管理员 """

    # 有：对象/无：None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, 'error.html', {"msg":"数据不存在"})
        return redirect('/admin/list/')

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)# 显示默认值 instance =row_object
        return render(request, 'change.html', {"form":form,"title":title})

    form = AdminEditModelForm(request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {"form":form,"title":title})


def admin_delete(request, nid):
    """ 删除管理员 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')

def admin_reset(request, nid):
    """ 重置管理员密码 """
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, 'error.html', {"msg":"数据不存在"})
        return redirect('/admin/list/')

    title = "重置密码--{}".format(row_object.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'change.html', {"form":form,"title": title})

    form = AdminResetModelForm(request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {"form":form,"title":title})