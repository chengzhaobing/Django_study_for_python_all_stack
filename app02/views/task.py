# 内置
import json
# 第三方
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt # 免除csrf_token认证
from django.http import JsonResponse
from django import forms
# 自定义
from app02.utils.bootstrap import BootStrapModelForm
from app02 import models
from app02.utils.pagination import Pagination




class TaskModelForm(BootStrapModelForm):
 class Meta:
    model = models.Task
    fields = '__all__'
    widgets = {
        "detail": forms.TextInput, # 常规文本框
        # "detail": forms.Textarea,    # 区域文本框
    }


@csrf_exempt
def task_list(request):
    """ 任务列表 """

    form = TaskModelForm()
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)

    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'task_list.html', context)

@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status":True,'data':[11,25,188,354]}
    # json_string = json.dumps(data_dict)
    # return HttpResponse(json_string)
    return JsonResponse(data_dict)



@csrf_exempt
def task_add(request):
    """ ajax案例--接受ajax请求 """
    print(request.POST)
    # < QueryDict: {'level': ['1'], 'title': ['sdvvds'], 'detail': ['sgsds'], 'user': ['8']} >

    # 1. 对用户发送过来的数据进行校验-----ModelForm校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse(json.dumps({"status":True}))

    data_dict = {"status":False, "error":form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

















