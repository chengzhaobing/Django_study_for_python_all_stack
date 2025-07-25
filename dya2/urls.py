
from django.contrib import admin
from django.urls import path

from app02 import views

# 因为这里我把原本views.py删掉了----自己新建了一个views文件夹，把不同的部分进行了拆分
# 所以这里需要更改path
from app02.views import depart, user, admin, account, task, order, chart, upload, profile, learning

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 首页
    path('', account.login),  # 根路径重定向到登录页
    path('index/', chart.chart_list),  # 首页仪表板

    # """ 部门管理 """

    # 部门信息
    path('depart/list/', depart.depart_list),

    # 添加部门
    path('depart/add/', depart.depart_add),

    # 删除部门
    path('depart/delete/', depart.depart_delete),

    #编辑部门
    # path('depart/edit/', views.depart_edit),

    # 正则传参法
    #https://127.0.0.1:8000/depart/1/edit/
    #https://127.0.0.1:8000/depart/2/edit/
    #https://127.0.0.1:8000/depart/3/edit/
    path('depart/<int:nid>/edit/', depart.depart_edit),

# """ 用户管理"""
    # 用户列表
    path('user/list/', user.user_list),

    # 新建用户
    path('user/add/', user.user_add),


    # 用modelform组件实现新建用户

    path('user/model/add/',user.user_model_add),

    # 编辑用户---定义携带的<int:nid>整型的nid
    path('user/<int:nid>/edit/', user.user_edit),

    # 删除用户
    path('user/<int:nid>/delete/', user.user_delete),


    # 管理员
    path('admin/list/', admin.admin_list),

    #添加管理员
    path('admin/add/', admin.admin_add),

    # 编辑管理员
    path("admin/<int:nid>/edit/", admin.admin_edit),

    #删除管理员
    path("admin/<int:nid>/delete/", admin.admin_delete),

    #重置密码
    path("admin/<int:nid>/reset/", admin.admin_reset),

    # 用户登录
    path("login/", account.login),
    
    # 用户注册
    path("register/", account.register),
    
    # 忘记密码
    path("forgot-password/", account.forgot_password),

    # 注销
    path('logout/', account.logout),

    # 图片验证码
    path('img/code/', account.img_code),

    # 任务管理
    path('task/list/', task.task_list),

    #--测试ajax
    path('task/ajax/', task.task_ajax),

    # ajax案例 -- 接受ajax请求
    path('task/add/', task.task_add),

    # 订单管理
    path('order/list/', order.order_list),
    # 接收用户请求
    path('order/add/', order.order_add),
    # 删除订单
    path('order/delete/', order.order_delete),
    # 编辑订单--获取默认显示数据
    path('order/detail/', order.order_detail),
    # 编辑订单--保存更新数据行--删除原数据并添加（而非单独的新增）
    path('order/edit/',order.order_edit),


    # 数据统计
    path('chart/list/', chart.chart_list),
    # 后台获取数据---生成柱状图
    path('chart/bar/', chart.chart_bar),
    # 后台获取数据---饼状图
    path('chart/pie/', chart.chart_pie),
    # 折线图
    path('chart/line/', chart.chart_line),

    # highcharts
    path('chart/highchart/', chart.highchart),

    # 文件上传
    path('upload/list/', upload.upload_list),

    # 文件上传案例---单个数据---excel单行上传
    path('depart/multi/', depart.depart_multi),

    # Form 混合数据上传
    path('upload/form/', upload.upload_form),
    
    # 个人资料和我的信息
    path('profile/', profile.personal_profile),
    path('profile/update/', profile.update_profile),
    path('my-info/', profile.my_info),
    
    # 学习总结和代码说明
    path('learning-summary/', learning.learning_summary),
    path('code-guide/', learning.code_guide),
]

