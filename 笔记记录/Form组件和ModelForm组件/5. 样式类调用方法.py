from django.shortcuts import render
from django import forms

# 自定义
from app02 import models

# Form组件方法
class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        # 原始样式封装，适合字段少的情况，widget=forms.TextInput(attrs={"class": "form-control"}),
        widget=forms.TextInput,
    )
    password = forms.CharField(
        label="密码",
        # 字段多就是用下列样式封装 widget=forms.PasswordInput(attrs={"class": "form-control"}),
        widget=forms.PasswordInput
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件,添加 样式
        for name, field in self.fields.items():
            # 字段中有属性，保留原属性，没有属性，才添加
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label
                }
