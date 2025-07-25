# 内置

# 第三方
from django.shortcuts import render
from django.http import JsonResponse


# 自定义


def chart_list(request):
    """ 数据统计页面 """

    return render(request, "chart_list.html")


def chart_bar(request):
    """ 后台获取数据 生成柱状图 """
    legend = ['6月销量', '7月销量', '8月销量']
    series_list = [
        {
            "name": '6月销量',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '7月销量',
            "type": 'bar',
            "data": [75, 80, 36, 48, 82, 63]
        },
        {
            "name": '8月销量',
            "type": 'bar',
            "data": [88, 50, 96, 50, 60, 52]
        },
    ]
    x_axis = ['2011年', '2012年', '2013年', '2014年', '2015年', '2016年']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    """ 后台获取数据 生成饼状图 """

    series_data = [
        {"value": 1048, "name": '成都'},
        {"value": 735, "name": '北京'},
        {"value": 580, "name": '长沙'},
        {"value": 484, "name": '深圳'},
        {"value": 300, "name": '上海'}
    ]
    result = {
        "status": True,
        "data": series_data
    }
    return JsonResponse(result)

def chart_line(request):
    """ 折线图 """
    x_axis = ['2010', '2011', '2012', '2013', '2014', '2015', '2016']
    legend = ['四川', '湖南', '广东', '江苏', '浙江']
    series_list = [
        {
            "data": [140, 232, 101, 264, 90, 340, 250]
        },
        {
            "data": [120, 282, 111, 234, 220, 340, 310]
        },
        {
            "data": [320, 132, 201, 334, 190, 130, 220]
        },
        {
            "data": [220, 402, 231, 134, 190, 230, 120]
        },
        {
            "data": [180, 352, 181, 184, 290, 280, 200]
        }
    ]
    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series': series_list,
            'x_axis': x_axis
        }
    }
    return JsonResponse(result)


def highchart(request):
    """ highchart """
    return render(request, "highchart.html")