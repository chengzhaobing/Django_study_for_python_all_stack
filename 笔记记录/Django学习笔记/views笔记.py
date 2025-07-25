from os.path import exists

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from app02 import models  # 导入models.py
from app02.utils import pagination # 导入分页组件 pagination.py
from app02.utils.pagination import Pagination
from app02.utils.bootstrap import BootStrapModelForm #导入bootstrap样式组件 bootstrap.py


""" 部门管理 """


# 部门信息表
def depart_list(request):
    """ 部门表"""

    queryset = models.Department.objects.all()  # 获取部门表所有数据

    page_object = Pagination(request, queryset)
    # print(queryset)   # <QuerySet [<Department: Department object (1)>, <Department: Department object (2)>]>
    # print(type(queryset)) # <class 'django.db.models.query.QuerySet'>
    # for obj in queryset:
    #     print(obj.title)
    # 把这个queryset传给html

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


""" 员工管理 """


def user_list(request):
    """ 用户管理 """

    # for i in range(100):
    # models.UserInfo.objects.create(name="陈都灵",password="khsiamahhi1..",age=26,salary=8500,create_time="1998-4-13",sex=0,depart_id=17)

    # 搜索功能
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        # data_dict = {"name__contains":value}
        data_dict["name"] = search_data
    # res = models.UserInfo.objects.filter(**data_dict)

    # [obj,obj,... , obj]
    # 设计分页 第一页：[0:10] 第二页[10:20] ... 第n页[n:n+10]

    # 通过 https://127.0.0.1:8000/user/list/?page=1,2,3....去切换页面

    from app02.utils.pagination import Pagination

    queryset = models.UserInfo.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "search_data": search_data,
        "page_string": page_object.html(),  # 页码
    }
    return render(request, "user_list.html", context)

    #
    # # page = int(request.GET.get("page", 1))  # 转换类型去计算
    # # page_size = 10
    # # start = (page - 1) * page_size
    # # end = page * page_size
    # #
    # # user_list = models.UserInfo.objects.filter(**data_dict)[page_object.start:page_object.end]
    # # # 数据总条数
    # # total_count = models.UserInfo.objects.filter(**data_dict).count()
    # # # 总页码
    # # total_page_count, div = divmod(total_count, page_size)
    # # if div:
    # #     total_page_count += 1
    #
    # # 计算出前5页后5页
    # static_page = 5
    # if total_page_count <= 2 * static_page + 1:
    #     # 数据库的数据比较少，没有达到11页那么就固定1-11页
    #     start_page = 1
    #     end_page = total_page_count
    # else:
    #     # 数据库数据较多
    #     if page <= static_page:
    #         # 当前页<5
    #         # 规范左侧页码为负值----当前页小于5时，左侧页码不应该动态变化
    #         start_page = 1
    #         end_page = 2 * static_page + 1
    #     else:
    #         if (page + static_page) > total_page_count:
    #             # 当前页 + 5 > 总页数
    #             # 规范右侧页码没有数据但有页码
    #             start_page = total_page_count - 2 * static_page
    #             end_page = total_page_count
    #         else:
    #             start_page = page - static_page
    #             end_page = page + static_page
    #
    # from django.utils.safestring import mark_safe  # 导入编译包，安全包--安全编译
    #
    # page_str_list = []
    #
    # # 首页
    # prev = '<li class="page-item"><a class="page-link" href="?page={}">首页</a></li>'.format(1)
    # page_str_list.append(prev)
    #
    # # 上一页
    # if page == 1:
    #     prev = '<li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(page)
    #     page_str_list.append(prev)
    # else:
    #     prev = '<li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(page - 1)
    #     page_str_list.append(prev)
    #
    # for i in range(start_page, end_page + 1):
    #     # 突出显示当前页
    #     if i == page:  # active 当前页
    #         ele = '<li class="page-item active"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = '<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
    #
    #     page_str_list.append(ele)
    # # 下一页
    # if page == total_page_count:
    #     prev = '<li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(page)
    #     page_str_list.append(prev)
    # else:
    #     prev = '<li class="page-item"><a class="page-link" href="?page={}">下一页</a></li>'.format(page + 1)
    #     page_str_list.append(prev)
    #
    # # 尾页
    # prev = '<li class="page-item"><a class="page-link" href="?page={}">尾页</a></li>'.format(total_page_count)
    # page_str_list.append(prev)
    # # 搜索页
    # search_page = """
    #     <li class="page-item">
    #         <form class="d-flex" method="get">
    #             <input name="page" style="width: 80px;height: 38px;position: relative;float: left;display: inline-block" class="form-control me-2"
    #                                type="search" placeholder="页码" aria-label="Search">
    #             <button style="height: 38px;width: 70px;" class="btn btn-outline-success" type="submit">跳转</button>
    #         </form>
    #     </li>
    # """
    # page_str_list.append(search_page)
    #
    # page_string = "".join(page_str_list)
    #
    # 打印结果
    # <li class="page-item"><a class="page-link" href="?page=1">1</a></li>
    # <li class="page-item"><a class="page-link" href="?page=2">2</a></li>
    # <li class="page-item"><a class="page-link" href="?page=3">3</a></li>
    # <li class="page-item"><a class="page-link" href="?page=4">4</a></li>
    # ...
    # <li class="page-item"><a class="page-link" href="?page=5">5</a></li><li class="page-item"><a class="page-link" href="?page=6">6</a></li><li class="page-item"><a class="page-link" href="?page=7">7</a></li><li class="page-item"><a class="page-link" href="?page=8">8</a></li><li class="page-item"><a class="page-link" href="?page=9">9</a></li><li class="page-item"><a class="page-link" href="?page=10">10</a></li><li class="page-item"><a class="page-link" href="?page=11">11</a></li><li class="page-item"><a class="page-link" href="?page=12">12</a></li><li class="page-item"><a class="page-link" href="?page=13">13</a></li><li class="page-item"><a class="page-link" href="?page=14">14</a></li><li class="page-item"><a class="page-link" href="?page=15">15</a></li><li class="page-item"><a class="page-link" href="?page=16">16</a></li><li class="page-item"><a class="page-link" href="?page=17">17</a></li><li class="page-item"><a class="page-link" href="?page=18">18</a></li><li class="page-item"><a class="page-link" href="?page=19">19</a></li><li class="page-item"><a class="page-link" href="?page=20">20</a></li><li class="page-item"><a class="page-link" href="?page=21">21</a></li><li class="page-item"><a class="page-link" href="?page=22">22</a></li><li class="page-item"><a class="page-link" href="?page=23">23</a></li><li class="page-item"><a class="page-link" href="?page=24">24</a></li><li class="page-item"><a class="page-link" href="?page=25">25</a></li><li class="page-item"><a class="page-link" href="?page=26">26</a></li><li class="page-item"><a class="page-link" href="?page=27">27</a></li><li class="page-item"><a class="page-link" href="?page=28">28</a></li><li class="page-item"><a class="page-link" href="?page=29">29</a></li><li class="page-item"><a class="page-link" href="?page=30">30</a></li><li class="page-item"><a class="page-link" href="?page=31">31</a></li>
    #
    # 产生的问题是没有编译----编译使用导入的安全包，进行编译
    # page_string = mark_safe("".join(page_str_list))

    # --------------------------------------------------------------------------------------

    # 打印查看格式
    # for obj in user_list:
    # 打印测试1
    # print(obj.name,obj.password,obj.age,obj.create_time)

    #     田曦薇 qwe12313 24 2025-07-19 00:00:00+00:00
    #     卢昱晓 qwe12313 24 2025-07-19 00:00:00+00:00
    #     陈都灵 qwe12313 24 2025-07-19 00:00:00+00:00
    #     时间格式不对

    #       打印测试2
    #         print(obj.name, obj.password, obj.age, obj.create_time, type(obj.create_time))

    #     打印create_time的类型为：
    # 田曦薇 qwe12313 24 2025-07-19 00:00:00+00:00 <class 'datetime.datetime'>
    # 卢昱晓 qwe12313 24 2025-07-19 00:00:00+00:00 <class 'datetime.datetime'>
    # 陈都灵 qwe12313 24 2025-07-19 00:00:00+00:00 <class 'datetime.datetime'>

    # 打印测试3：使用strftime 将 time--转-->str
    # print(obj.name, obj.password, obj.age,
    #       obj.create_time.strftime("%Y-%m-%d"), type(obj.create_time))

    # 田曦薇 qwe12313 24 2025-07-19 <class 'datetime.datetime'>
    # 卢昱晓 qwe12313 24 2025-07-19 <class 'datetime.datetime'>
    # 陈都灵 qwe12313 24 2025-07-19 <class 'datetime.datetime'>

    # 打印测试4: 性别字段回显---get_字段名_display()
    # """
    # models.py中userinfo表的性别字段定义
    #
    # gender_choice = (
    # (1, "男"),
    # (0, "女"),
    # )
    #
    # sex = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)
    # """
    # print(obj.name,obj.sex,obj.get_sex_display())

    # 田曦薇 0 女
    # 卢昱晓 0 女
    # 陈都灵 0 女

    # 打印测试5 : 外键字段回显--Django内置方法,外键字段.外键表字段(department表对照字段)
    # """
    # models.py中userinfo表的外键字段定义
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # """
    # print(obj.name, obj.depart_id, obj.depart.title)

    # 田曦薇 11 文艺部
    # 卢昱晓 11 文艺部
    # 陈都灵 11 文艺部


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


from django import forms


class UserModelForm(forms.ModelForm):
    # 其他校验方式:
    name = forms.CharField(min_length=2, label="用户名")  # 校验1,校验用户名长度

    # 否则出发django自带错误校验提示:Ensure this value has at least 2 characters (it has 1).

    # password = forms.CharField(label="密码", validators= 编写正常表达式) #校验2

    class Meta:
        model = models.UserInfo

        fields = "__all__"  # 显示取UserInfo数据表定义的全部字段
        # fields = ["name","age","password"] # 显示某个字段
        # exclude = [''] 排除某个字段，其他全部显示

        # 法1: widgets插件添加样式繁琐
        # widgets = {
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        #     "password": forms.TextInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    # 法2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件,添加 样式
        for name, field in self.fields.items():
            # 某个字段不想加样式 (一直循环进来判断,条件成立,continue直接 跳转到for循环,而不执行后续的)

            # 这里例如 create_time字段不想加样式---可知for循环内的name不属于字段名
            # if name == "create_time":
            #     continue

            # 下面两种写法相等
            # field.widget.attrs["class"] = "form-control"
            field.widget.attrs = {"class": "form-control"}

    # 法1---校验字段方法--正则表达法
    age = forms.IntegerField(
        label="年龄",
        validators=[RegexValidator(regex=r"^[1-9][0-9]$")],  # 自行替换相关符合规则的校验
    )

    # 法2--校验字段-- 钩子方法 ： clean_字段名 ---可以进行字段校验
    def clean_name(self):
        # 校验age年龄字段 不少于2位数 不超过3位数
        salary_data = self.cleaned_data["salary"]
        if (len(salary_data) > 1 and len(salary_data) < 3):
            return ValidationError("请输入正确年龄！")
        return salary_data
        # ---用户名已存在
        name_data = self.cleaned_data["name"]
        exist = models.UserInfo.objects.filter(name=name_data).exists()  # 存在返回True
        # ---排除自身以外，存在就报错
        # self.instance.pk # 当前编辑行的ID--instance是对象
        # exist = models.UserInfo.objects.exclude(id=self.instance.pk).filter(name=name_data).exists()

        if exist:
            raise ValidationError("用户名已存在！")
        return name_data


def user_model_add(request):
    # GET请求

    if request.method == "GET":
        form = UserModelForm()

        return render(request, "user_model_add.html", {"form": form})

    # 通过{"form":form}传过去后,可以通过
    #     {{ form.name.label }}:{{ form.name }}
    #     {{ form.password.label }}:{{ form.password }}
    #     {{ form.age.label }}:{{ form.age }}

    # 画出input框,其中带有label为标签名,即verbose名

    # POST请求

    # 获取数据---+ ---数据校验
    form = UserModelForm(data=request.POST)  # request.POST指用户提交的所有数据----传入UserModelForm类校验
    if form.is_valid():
        print(form.cleaned_data)  # 打印所有校验成功的信息
        # {'name': 'cheng', 'password': 'eyshjk123', 'age': 52, 'salary': Decimal('5000'), 'create_time': datetime.datetime(2011, 8, 6, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'sex': 1, 'depart': <Department: 市场部>}
        # 校验成功拿到所有信息
        # 存入数据库
        # 1. 原始保存到数据库方法
        # models.UserInfo.objects.create(...)
        # 2.Django内置保存到数据库方法
        form.save()
        return redirect('/user/list/')

    # 校验失败,显示错误信息

    # print(form.errors) # 打印所有错误信息
    return render(request, "user_model_add.html", {"form": form})


# /user/(nid)/eidt/
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
        # {'name': 'cheng', 'password': 'eyshjk123', 'age': 52, 'salary': Decimal('5000'), 'create_time': datetime.datetime(2011, 8, 6, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'sex': 1, 'depart': <Department: 市场部>}
        # 校验成功拿到所有信息
        # 存入数据库
        # 1. 原始保存到数据库方法
        # models.UserInfo.objects.create(...)
        # 2.Django内置保存到数据库方法

        form.save()  # 默认保存用户输入的所有数据
        return redirect('/user/list/')
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

# 注：删除和编辑用户都需要，在urls.py中引入  /<int:nid>/
