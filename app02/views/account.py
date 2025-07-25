# 内置
from io import BytesIO

from django.forms import TextInput
# 第三方
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse

# 自定义
from app02 import models
from app02.utils.bootstrap import BootstrapForm
from app02.utils.code import check_code

# # ModelForm组件方法 ---- （这次采用Form，在这里功能一致）
# class LoginModelForm(forms.Form):
#     class Meta:
#         model = models.Admin
#         fields = ['username', 'password']

# Form组件方法
class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True, #必填不能为空(默认True)
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True,
    )
    code = forms.CharField(
        label="图片验证码",
        widget=forms.TextInput,
        required=True,
    )


    # 钩子方法
    def clean_password(self):
        from app02.utils.encrypt import md5
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class RegisterForm(BootstrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True,
        min_length=3,
        max_length=20,
        help_text="用户名长度3-20个字符"
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True,
        min_length=6,
        help_text="密码长度至少6个字符"
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,
        required=True,
    )
    code = forms.CharField(
        label="图片验证码",
        widget=forms.TextInput,
        required=True,
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # 检查用户名是否已存在
        if models.Admin.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("两次输入的密码不一致")
        return confirm_password

    def clean_password(self):
        from app02.utils.encrypt import md5
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class ForgotPasswordForm(BootstrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True,
        help_text="请输入您的用户名"
    )
    new_password = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput,
        required=True,
        min_length=6,
        help_text="新密码长度至少6个字符"
    )
    confirm_password = forms.CharField(
        label="确认新密码",
        widget=forms.PasswordInput,
        required=True,
    )
    code = forms.CharField(
        label="图片验证码",
        widget=forms.TextInput,
        required=True,
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # 检查用户名是否存在
        if not models.Admin.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名不存在")
        return username

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("两次输入的密码不一致")
        return confirm_password

    def clean_new_password(self):
        from app02.utils.encrypt import md5
        pwd = self.cleaned_data.get("new_password")
        return md5(pwd)


def login(request):
    """ 用户登录 """

    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # form中用下列方法表示验证成功，获取到用户名和密码
        # print(form.cleaned_data)

        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get('image_code', "")
        # 验证码校验
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})

        # 去数据库校验用户名和密码是否正确, 获取用户对象
        # 法1
        # models.Admin.objects.filter(username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password')).first()
        # 法2：                                  # 这里作对比不能有其他数据，所有用pop将图片验证码先拿出去
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误") # 在密码框下显示
            return render(request, "login.html", {"form": form})

        # return HttpResponse("提交成功")
        # 用户名密码正确登录后
        # 网站生成随机字符串；写到用户浏览器的cookie中，再写入Session中
        # request.session["info"] ="hello Session"

        # info = request.session['info'] # 把获取当前的登录信息 ---把用户名实时传送到模板中，显示各自的登录名
        # print(info)

        request.session["info"] = {'id':admin_object.id,'name':admin_object.username}
        #登录成功---session7天不过期----用户信息保存7天
        request.session.set_expiry(60*60*24*7) # 7天免登录
        return redirect("/admin/list/")


    return render(request, "login.html", {"form": form})





########################################################################
# 这里很神奇-----在login.html登录模板中，验证码图片<img src="/img/code/"> </img>
# 在img标签的src路径中放的是一个网页
def img_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数生成图片
    img, code_string = check_code()
    # 写入到自己的Session中（以便于后续获取验证码再进行校验）
    request.session["image_code"] = code_string
    # 给session设置60s超时----过60s后无效
    request.session.set_expiry(60)

    stream = BytesIO()  # 创建一个内存文件
    img.save(stream, 'png') # 写入内存文件
    stream.getvalue()
    return HttpResponse(stream.getvalue()) #获取到图片传到前端页面

# 也就是说 网页可以被嵌套进 任何带路径的标签内
########################################################################








def register(request):
    """ 用户注册 """
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        # 验证码校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'register.html', {'form': form})
        
        # 移除确认密码字段
        form.cleaned_data.pop('confirm_password')
        
        # 创建用户
        models.Admin.objects.create(**form.cleaned_data)
        return redirect('/login/')
    
    return render(request, 'register.html', {'form': form})


def forgot_password(request):
    """ 忘记密码 """
    if request.method == "GET":
        form = ForgotPasswordForm()
        return render(request, 'forgot_password.html', {'form': form})
    
    form = ForgotPasswordForm(data=request.POST)
    if form.is_valid():
        # 验证码校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'forgot_password.html', {'form': form})
        
        # 更新密码
        username = form.cleaned_data.get('username')
        new_password = form.cleaned_data.get('new_password')
        models.Admin.objects.filter(username=username).update(password=new_password)
        
        return redirect('/login/')
    
    return render(request, 'forgot_password.html', {'form': form})


def logout(request):
    """ 注销 """

    request.session.clear()
    return redirect("/login/")