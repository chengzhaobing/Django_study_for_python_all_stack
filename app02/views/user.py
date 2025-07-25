
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from app02 import models  # 导入models.py
from app02.utils.pagination import Pagination

# 用到什么去utils组件文件夹内导入什么，继续导入到后
from app02.utils.form import UserModelForm



""" 员工管理 """
def user_list(request):
    """ 用户管理 """

    # 搜索功能
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        # data_dict = {"name__contains":value}
        data_dict["name__contains"] = search_data


    from app02.utils.pagination import Pagination

    queryset = models.UserInfo.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "search_data": search_data,
        "page_string": page_object.html(),  # 页码
    }
    return render(request, "user_list.html", context)


def user_add(request):
    """ 新建用户(原始方式) """

    if request.method == "GET":
        # 提前定义一个字典,再传给模板文件
        context = {
            'sex_choice': models.UserInfo.sex_choice,  # 这是一个元组数据,用数字取值
            'depart_list': models.Department.objects.all(),
        }

        return render(request, 'user_add.html', context)

    # 如果是POST 即动态提交,获取输入框传过来的数据

    username = request.POST.get("name")  # 左边赋值,右边的为输入框内的名字----即name标签
    password = request.POST.get("pwd")
    age = request.POST.get("age")
    gender_id = request.POST.get("sex")
    salary = request.POST.get("money")
    create_time = request.POST.get("time")
    depart_id = request.POST.get("depart")

    # 将获取到的数据添加到数据中(左边数据库字段名=右边传入参数名,,
    # 实际中最好把所有的名字都命名为相同名,这样不易出错,但不易区分
    models.UserInfo.objects.create(name=username, password=password,
                                   age=age, sex=gender_id, salary=salary,
                                   create_time=create_time, depart_id=depart_id)

    # 添加成功后返回到用户列表页面
    return redirect('/user/list/')


def user_model_add(request):
    # GET请求

    if request.method == "GET":
        form = UserModelForm()

        return render(request, "user_model_add.html", {"form": form})

    # 获取数据---+ ---数据校验
    form = UserModelForm(data=request.POST)  # request.POST指用户提交的所有数据----传入UserModelForm类校验
    if form.is_valid():
        print(form.cleaned_data)  # 打印所有校验成功的信息

        form.save()
        return redirect('/user/list/')

    # 校验失败,显示错误信息

    # print(form.errors) # 打印所有错误信息
    return render(request, "user_model_add.html", {"form": form})


def user_edit(request, nid):
    """
    编辑用户
    需求:
    1.点击编辑，将用户id携带走，跳转到编辑页面
    2. 编辑页面设置获取id用户的默认值
    3. 提交跳转到 user_list.html

    """

    # 1.设置编辑页面input框内默认值----（在input框设置value参数即为默认值）
    row_list = models.UserInfo.objects.filter(id=nid).first()  # (对象)

    if request.method == "GET":
        # instance=row_list 表示 默认显示在input框内的的数据
        form = UserModelForm(instance=row_list)
        return render(request, "user_edit.html", {"form": form})

    # request.POST指用户提交的所有数据----传入UserModelForm类校验
    # instance = row_data -------------表示更新的地址，保存的地址
    form = UserModelForm(data=request.POST, instance=row_list)
    if form.is_valid():
        print(form.cleaned_data)  # 打印所有校验成功的信息


        form.save()  # 默认保存用户输入的所有数据
        return redirect('/user/list/')
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

