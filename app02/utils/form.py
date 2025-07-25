from django.core.exceptions import ValidationError

from django import forms
from app02 import models  # 导入models.py
from app02.utils.bootstrap import BootStrapModelForm #导入bootstrap样式组件 bootstrap.py



class UserModelForm(BootStrapModelForm):
    # 其他校验方式:
    name = forms.CharField(min_length=2, label="用户名")  # 校验1,校验用户名长度

    class Meta:
        model = models.UserInfo

        fields = "__all__"  # 显示取UserInfo数据表定义的全部字段


    def clean_name(self):
        # 校验age年龄字段 不少于2位数 不超过3位数
        salary_data = self.cleaned_data["salary"]
        if (len(salary_data) > 1 and len(salary_data) < 3):
            return ValidationError("请输入正确年龄！")
        return salary_data
        # ---用户名已存在
        name_data = self.cleaned_data["name"]
        exist = models.UserInfo.objects.filter(name=name_data).exists()  # 存在返回True

        if exist:
            raise ValidationError("用户名已存在！")
        return name_data
