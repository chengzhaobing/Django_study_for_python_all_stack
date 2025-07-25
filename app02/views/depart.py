
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from app02 import models  # 导入models.py
from app02.utils.pagination import Pagination

# 用到什么去utils组件文件夹内导入什么，继续导入到后
from app02.utils.form import UserModelForm



""" 部门管理 """


# 部门信息表
def depart_list(request):
    """ 部门表"""

    queryset = models.Department.objects.all()  # 获取部门表所有数据

    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,
        "page_string":page_object.html(),
    }

    return render(request, "depart_list.html", context)


def depart_add(request):
    """ 添加部门页面 """
    if request.method == "GET":
        return render(request, "depart_add.html")

    # else: #(POST)
    # 用户提交的POST，开始获取数据（判断为空暂时不考虑，后续用组件解决）
    depart_info = request.POST.get("title")  # 这里是最重要的 修复了一辈子 # 这里的tile接受的是输入框的名称必须设置输入框名称

    # 保存到数据库
    models.Department.objects.create(title=depart_info)

    # 重定向回部门信息表
    return redirect('/depart/list/')


def depart_delete(request):
    """ 删除部门 """

    # http://127.0.0.1:8000/depart/list/?nid=2 删除id为2的
    """ *重点* 给删除标签加一个目的地址"""

    # 获取id
    nid = request.GET.get("nid")
    print(nid)

    # 删除id
    models.Department.objects.filter(id=nid).delete()

    # 删完重定向回来
    return redirect('/depart/list/')


def depart_edit(request, nid):
    """ 编辑部门 """
    if request.method == "GET":
        # 获取传过来的nid
        row_list = models.Department.objects.filter(id=nid).first()  # 获取当前行
        print("id = ", row_list.id, "title = ", row_list.title)

        return render(request, "depart_edit.html", {"row_list": row_list})

    # 获取用户提交的信息
    title = request.POST.get("title")

    # 获取到数据对数据库进行更新
    models.Department.objects.filter(id=nid).update(title=title)

    return redirect('/depart/list/')

def depart_multi(request):
    """ 文件上传案例---单个数据  """
    from openpyxl import load_workbook
    # 1. 获取用户上传的文件对象
    from django.core.files.uploadedfile import InMemoryUploadedFile
    file_obj = request.FILES.get("upload_file_excel") # 上传文件的input框name
    # print(type(file_obj))
    # print(file_obj.name)

    # 2. 上传的文件对象传递给openpyxl，使用openpyxl读取excel
    wb = load_workbook(file_obj)
    sheet = wb.worksheets[0]

    # 3. 循环获取每一行的数据
    for row in sheet.iter_rows(min_row=2,min_col=2): # 去除第一行（标题行）,去除第一列（ID列）
        # print(row) # 循环打印行对象
        text = row[0].value
        # print(text)
        # 添加到数据库
        exist = models.Department.objects.filter(title=text).exists()
        if not exist:
            models.Department.objects.create(title=text)
    return redirect('/depart/list/')

