from django.db import models

# Create your models here.

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="标题",max_length=32)

    # 为了利用ModelForm组件在模板文件中循环打印出 部门对象下的内部值,定义一个__str__方法

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """ 员工信息表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    salary = models.DecimalField(verbose_name="薪资", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间") ## DateTimeField包含时分秒
    create_time = models.DateField(verbose_name="入职时间") ## 年月日
    sex_choice = (
        (1, "男"),
        (0, "女"),
    )
    sex = models.SmallIntegerField(verbose_name="性别", choices=sex_choice)
    # 用1，2小整型表示性别，choices去对照性别

    # 取值的对应的时候，Django提供一个函数
    # get_字段名称_display()
    #          ||
#     get_sex_display()
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)

class Admin(models.Model):
    """ 管理员信息表 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    # 定制被作为外键导入的时候--显示对象obj而不显示对象内的值的问题
    def __str__(self):
        return self.username

class Task(models.Model):
    """ 任务表 """
    level_choice = (
        (1,"紧急"),
        (2,"重要"),
        (3,"临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choice,default=1)
    title = models.CharField(verbose_name="标题",max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单表 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称",max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1,"待支付"),
        (2,"已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)