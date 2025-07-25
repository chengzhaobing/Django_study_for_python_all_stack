from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from app02 import models
from app02.utils.pagination import Pagination
from app02.utils.form import UserModelForm
from app02.utils.encrypt import md5
from django.core.exceptions import ValidationError
import json


def personal_profile(request):
    """个人资料页面"""
    # 获取当前登录用户信息
    user_id = request.session.get('info', {}).get('id')
    if not user_id:
        return render(request, 'error.html', {'error_msg': '请先登录'})
    
    # 获取用户详细信息
    try:
        user_info = models.Admin.objects.get(id=user_id)
    except models.Admin.DoesNotExist:
        return render(request, 'error.html', {'error_msg': '用户不存在'})
    
    # 获取用户统计信息
    user_stats = {
        'total_tasks': models.Task.objects.filter(user=user_info).count(),
        'urgent_tasks': models.Task.objects.filter(user=user_info, level=1).count(),
        'important_tasks': models.Task.objects.filter(user=user_info, level=2).count(),
        'total_orders': models.Order.objects.filter(admin=user_info).count(),
    }
    
    # 最近的任务
    recent_tasks = models.Task.objects.filter(user=user_info).order_by('-id')[:5]
    
    # 最近的订单
    recent_orders = models.Order.objects.filter(admin=user_info).order_by('-id')[:5]
    
    context = {
        'user_info': user_info,
        'user_stats': user_stats,
        'recent_tasks': recent_tasks,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'personal_profile.html', context)


def my_info(request):
    """我的信息页面 - 技术栈和项目介绍"""
    # 技术栈信息
    tech_stack = {
        'backend': [
            {'name': 'Python', 'level': 95, 'description': '主要编程语言，熟练掌握面向对象编程、函数式编程等'},
            {'name': 'Django', 'level': 90, 'description': 'Web框架，熟练使用MTV模式、ORM、中间件等'},
            {'name': 'Flask', 'level': 85, 'description': '轻量级Web框架，适用于API开发和微服务'},
            {'name': 'FastAPI', 'level': 80, 'description': '现代化API框架，支持异步编程和自动文档生成'},
            {'name': 'MySQL', 'level': 88, 'description': '关系型数据库，熟练使用SQL查询优化和索引设计'},
            {'name': 'Redis', 'level': 82, 'description': '缓存数据库，用于会话管理和数据缓存'},
        ],
        'frontend': [
            {'name': 'JavaScript', 'level': 88, 'description': 'ES6+语法，熟练使用异步编程和模块化开发'},
            {'name': 'Vue.js', 'level': 85, 'description': '前端框架，组件化开发和状态管理'},
            {'name': 'React', 'level': 80, 'description': 'React Hooks、Redux状态管理'},
            {'name': 'HTML5/CSS3', 'level': 92, 'description': '响应式设计、CSS Grid、Flexbox布局'},
            {'name': 'Bootstrap', 'level': 90, 'description': 'UI框架，快速构建响应式界面'},
            {'name': 'jQuery', 'level': 85, 'description': 'DOM操作和Ajax请求处理'},
        ],
        'tools': [
            {'name': 'Git', 'level': 90, 'description': '版本控制，分支管理和团队协作'},
            {'name': 'Docker', 'level': 75, 'description': '容器化部署和微服务架构'},
            {'name': 'Linux', 'level': 80, 'description': '服务器运维和Shell脚本编写'},
            {'name': 'Nginx', 'level': 78, 'description': 'Web服务器配置和负载均衡'},
            {'name': 'PyCharm', 'level': 95, 'description': 'Python集成开发环境'},
            {'name': 'VS Code', 'level': 88, 'description': '轻量级代码编辑器，插件生态丰富'},
        ]
    }
    
    # 项目经验
    projects = [
        {
            'name': '企业管理信息系统',
            'description': '基于Django框架开发的企业级管理系统，包含用户管理、部门管理、任务管理、订单管理等模块',
            'tech': ['Python', 'Django', 'MySQL', 'Bootstrap', 'jQuery'],
            'features': [
                '用户权限管理和身份认证',
                '数据可视化图表展示',
                'Ajax异步数据交互',
                '文件上传和处理',
                '响应式界面设计'
            ],
            'github': 'https://github.com/username/django-management-system',
            'demo': 'http://demo.example.com'
        },
        {
            'name': 'RESTful API服务',
            'description': '使用FastAPI构建的高性能API服务，支持异步处理和自动文档生成',
            'tech': ['Python', 'FastAPI', 'PostgreSQL', 'Redis', 'Docker'],
            'features': [
                '异步请求处理',
                '自动API文档生成',
                'JWT身份验证',
                '数据库连接池',
                'Docker容器化部署'
            ],
            'github': 'https://github.com/username/fastapi-service',
            'demo': 'http://api.example.com/docs'
        },
        {
            'name': '数据分析平台',
            'description': '基于Python的数据分析和可视化平台，支持多种数据源和图表类型',
            'tech': ['Python', 'Pandas', 'NumPy', 'Matplotlib', 'ECharts'],
            'features': [
                '多数据源接入',
                '实时数据处理',
                '交互式图表展示',
                '报表自动生成',
                '数据导出功能'
            ],
            'github': 'https://github.com/username/data-analysis-platform',
            'demo': 'http://analytics.example.com'
        }
    ]
    
    # 代码示例
    code_examples = [
        {
            'title': 'Django中间件实现',
            'language': 'python',
            'code': '''class AuthMiddleware:
    """用户认证中间件"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 排除不需要登录的路径
        if request.path_info in ["/login/", "/img/code/", "/"]:
            return self.get_response(request)
        
        # 检查用户登录状态
        info = request.session.get("info")
        if not info:
            return redirect('/login/')
        
        return self.get_response(request)'''
        },
        {
            'title': 'Ajax数据交互',
            'language': 'javascript',
            'code': '''function bindBtnAddEvent() {
    $('#btnAdd').click(function() {
        // 清空表单
        $('#myModal form')[0].reset();
        $('#myModal').modal('show');
    });
    
    $('#btnSave').click(function() {
        $.ajax({
            url: "/task/add/",
            type: "post",
            data: $('#myModal form').serialize(),
            dataType: "JSON",
            success: function(res) {
                if (res.status) {
                    location.reload();
                } else {
                    alert(res.error);
                }
            }
        });
    });
}'''
        },
        {
            'title': 'ECharts图表配置',
            'language': 'javascript',
            'code': '''function initLineChart() {
    var myChart = echarts.init(document.getElementById('line'));
    
    $.get('/chart/line/', function(res) {
        var option = {
            title: { text: '销售趋势分析' },
            tooltip: { trigger: 'axis' },
            xAxis: {
                type: 'category',
                data: res.legend
            },
            yAxis: { type: 'value' },
            series: [{
                data: res.series,
                type: 'line',
                smooth: true,
                areaStyle: {}
            }]
        };
        myChart.setOption(option);
    });
}'''
        }
    ]
    
    context = {
        'tech_stack': tech_stack,
        'projects': projects,
        'code_examples': code_examples,
    }
    
    return render(request, 'my_info.html', context)


def update_profile(request):
    """更新个人资料"""
    if request.method == 'POST':
        user_id = request.session.get('info', {}).get('id')
        if not user_id:
            return JsonResponse({'status': False, 'error': '请先登录'})
        
        try:
            user = models.Admin.objects.get(id=user_id)
            
            # 更新用户信息
            user.username = request.POST.get('username', user.username)
            user.save()
            
            # 更新session信息
            request.session['info']['name'] = user.username
            
            return JsonResponse({'status': True, 'message': '更新成功'})
        except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)})
    
    return JsonResponse({'status': False, 'error': '请求方法错误'})