

from django import forms

"""
其他地方继承样式方法：


class LoginForm(forms.Form): 就不用这样了

而是：
from app02.utils import BootstrapForm

class LoginForm(BootstrapForm):

from app02.utils import BootstrapModelForm

class LoginForm(BootstrapModelForm):

"""


# 由于下面两个类内容相同只是继承者不同，
# 简化方法----写一个公共类：

class BootStrap:
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件,添加 样式
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            # 字段中有属性，保留原属性，没有属性，才添加
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label
                }


                        # 继承 forms.ModelForm---针对所有ModelForm


    # BootStrapForm 继承BootStrap类 、forms.Form类
class BootStrapModelForm(BootStrap,forms.ModelForm):
    pass

    # BootStrapForm 继承BootStrap类 、forms.ModelForm类
class BootstrapForm(BootStrap, forms.Form):
    pass






# class BootStrapModelForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 循环找到所有插件,添加 样式
#         for name, field in self.fields.items():
#             # 字段中有属性，保留原属性，没有属性，才添加
#             if field.widget.attrs:
#                 field.widget.attrs['class'] = 'form-control'
#                 field.widget.attrs['placeholder'] = field.label
#             else:
#                 field.widget.attrs = {
#                     'class': 'form-control',
#                     'placeholder': field.label
#                 }
#
#
#                 # 继承 forms.Form---针对所有Form
#
# class BootStrapForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 循环找到所有插件,添加 样式
#         for name, field in self.fields.items():
#             # 字段中有属性，保留原属性，没有属性，才添加
#             if field.widget.attrs:
#                 field.widget.attrs['class'] = 'form-control'
#                 field.widget.attrs['placeholder'] = field.label
#             else:
#                 field.widget.attrs = {
#                     'class': 'form-control',
#                     'placeholder': field.label
#                 }
