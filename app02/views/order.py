# 内置
import json
import random
from datetime import datetime
from os.path import exists

# 第三方
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
# 自定义
from app02 import models
from app02.utils.bootstrap import BootStrapModelForm
from app02.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        exclude = ['oid','admin']




def order_list(request):
    """ 订单列表 """
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset, #生成分页数据
        "page_string": page_object.html(),     #生成页码
    }

    form = OrderModelForm()
    return render(request, "order_list.html", context)

@csrf_exempt
def order_add(request):
    """ 新建订单(Ajax请求) """
    form = OrderModelForm(data = request.POST)
    if form.is_valid():
        # 订单号 ： 需要额外增加一些不是用户输入的值（自己计算出来的）
        # 保存前生成随机订单编号，不然oid为空
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,9999))

        # 管理员： 固定设置管理员id
        # form.instance.admin = 当前登录的系统管理员的ID
        form.instance.admin_id  = request.session["info"]["id"] #登录信息会保存到session中---从session获取
        #保存到数据库中
        form.save()
        # return HttpResponse(json.dumps({'status': True}))
        return JsonResponse({'status': True})

    return JsonResponse({'status': False,"error": form.errors})



def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False,"error":"数据不存在"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

def order_detail(request):
    """ 根据id获取详细信息 """
    # #方法1：
    # uid = request.GET.get('uid')
    # row_object = models.Order.objects.filter(id=uid).first()
    # if not row_object:
    #     return JsonResponse({"status":False, "error":"数据不存在"})
    #
    # # 从数据库中获取到一个对象 row_object
    # result ={
    #     "status": True,
    #     "data":{
    #         "title":row_object.title,
    #         "price":row_object.price,
    #         "status": row_object.status,
    #     }
    # }
    # # 返回结果给前端
    # return JsonResponse(result)

    # 方法2：
    uid = request.GET.get('uid')
    # values("title", "price", "status", "oid")  # 字典，｛“title”:xx,"price":xx｝
    row_object = models.Order.objects.filter(id=uid).values("title","price","status").first()
    if not row_object:
        return JsonResponse({"status":False, "error":"数据不存在"})

    # 从数据库中获取到一个对象 row_object
    result ={
        "status": True,
        "data":row_object, # 使用values直接返回字典/不用自己构造
    }
    # 返回结果给前端
    return JsonResponse(result)

@csrf_exempt
def order_edit(request):
    """ 编辑订单 """

    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status":False, "tips":"数据不存在,请刷新重试"})

    form = OrderModelForm(data = request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({"status": False, "all_error": "数据不存在","error":form.errors})





