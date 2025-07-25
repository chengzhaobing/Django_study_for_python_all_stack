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
    
    # 个人标签
    personal_tags = [
        {'name': '全栈开发', 'description': '前后端技术并重', 'icon': 'bi bi-stack', 'color': '#667eea'},
        {'name': '持续学习', 'description': '保持技术敏感度', 'icon': 'bi bi-book', 'color': '#f093fb'},
        {'name': '团队协作', 'description': '良好的沟通能力', 'icon': 'bi bi-people', 'color': '#4ecdc4'},
        {'name': '问题解决', 'description': '善于分析和解决问题', 'icon': 'bi bi-lightbulb', 'color': '#45b7d1'},
        {'name': '代码质量', 'description': '注重代码规范和质量', 'icon': 'bi bi-code-slash', 'color': '#96ceb4'},
        {'name': '用户体验', 'description': '关注产品用户体验', 'icon': 'bi bi-heart', 'color': '#feca57'},
        {'name': '技术分享', 'description': '乐于分享技术经验', 'icon': 'bi bi-share', 'color': '#ff6b6b'},
        {'name': '创新思维', 'description': '勇于尝试新技术', 'icon': 'bi bi-rocket', 'color': '#a55eea'},
    ]
    
    # 学习历程数据
    learning_journey = [
        {
            'category': 'Django基础',
            'title': 'Django框架核心概念与应用',
            'summary': '''通过系统学习Django框架，掌握了Web开发的核心概念。学习了MVC架构模式、URL路由、视图函数、模板系统、ORM数据库操作等核心功能。
            
            重点学习了Django的模板语法，包括变量渲染、循环语句、条件判断等。掌握了如何在模板中使用内置函数，如get_sex_display()获取选择字段的显示值，以及时间格式化的date过滤器使用。''',
            'key_points': [
                'Django模板语法中函数调用不需要括号',
                '使用date过滤器进行时间格式化：{{ obj.create_time|date:"Y-m-d H:i:s" }}',
                'get_display()方法获取choices字段的显示值',
                'URL传参的两种方式：查询参数和路径参数',
                'Django内置的性别等选择字段的处理方法'
            ]
        },
        {
            'category': 'Form组件',
            'title': 'Form组件和ModelForm组件深入应用',
            'summary': '''深入学习Django的Form组件和ModelForm组件，这是Django中处理表单的核心工具。Form组件提供了表单验证、数据清洗、HTML渲染等功能。
            
            ModelForm组件基于Model自动生成表单，大大简化了开发流程。学习了钩子方法的使用，可以在数据验证过程中添加自定义逻辑。掌握了样式类的调用方法，让表单具有更好的视觉效果。''',
            'key_points': [
                'Form组件提供数据验证和HTML渲染功能',
                'ModelForm基于Model自动生成表单字段',
                '钩子方法clean_字段名()用于自定义验证逻辑',
                'BootstrapForm样式类统一表单外观',
                '表单错误信息的前端显示和处理'
            ]
        },
        {
            'category': 'Ajax技术',
            'title': 'Ajax异步交互与前后端数据传输',
            'summary': '''学习Ajax技术实现前后端异步交互，提升用户体验。掌握了模态框的实现方法，Ajax错误信息处理，以及Ajax删除操作的实现。
            
            重点学习了后端数据库数据获取并传给前端的方法，包括JSON序列化的使用。理解了Ajax请求的完整流程：前端发送请求 → 后端处理 → 返回JSON数据 → 前端处理响应。''',
            'key_points': [
                'jQuery的$.ajax()方法进行异步请求',
                '使用$.each()循环处理错误信息显示',
                'JSON序列化将Python对象转换为前端可用数据',
                '模态框与Ajax结合实现无刷新操作',
                'CSRF令牌在Ajax请求中的处理'
            ]
        },
        {
            'category': '浏览器交互',
            'title': '浏览器与网站交互机制',
            'summary': '''深入理解浏览器与网站的交互机制，包括HTTP请求响应流程、Session会话管理、Cookie机制等。学习了Django中Session的不同存储方式。
            
            重点学习了图片验证码的实现，使用Pillow库绘制验证码图片，包括随机字符生成、图片绘制、干扰线添加等技术。掌握了验证码在用户注册、登录等场景中的应用。''',
            'key_points': [
                'HTTP请求响应的完整流程',
                'Session在数据库、缓存、文件中的存储方式',
                'Pillow库绘制图片验证码的方法',
                '随机验证码生成：数字、字母、混合模式',
                '验证码的前端刷新和后端验证机制'
            ]
        },
        {
            'category': '前端图表',
            'title': '数据可视化与图表展示',
            'summary': '''学习前端图表库的使用，包括Chart.js、Highcharts等。掌握了柱状图、饼状图、折线图等常用图表类型的实现方法。
            
            学习了后端数据处理和前端图表渲染的完整流程，包括数据查询、JSON序列化、前端Ajax获取数据、图表配置和渲染等步骤。''',
            'key_points': [
                '多种图表类型的实现：柱状图、饼状图、折线图',
                '后端数据统计和聚合查询',
                'Chart.js和Highcharts图表库的使用',
                'Ajax动态获取图表数据',
                '响应式图表设计和配置优化'
            ]
        },
        {
            'category': '文件操作',
            'title': '文件上传与处理技术',
            'summary': '''学习Django中的文件上传处理，包括单文件上传、多文件上传、Excel文件解析等。掌握了文件存储、文件验证、文件类型检查等关键技术。
            
            重点学习了Excel文件的读取和写入，使用openpyxl库处理Excel数据，实现了批量数据导入导出功能。''',
            'key_points': [
                'Django文件上传的request.FILES处理',
                'openpyxl库读写Excel文件',
                '文件类型验证和大小限制',
                '批量数据导入的事务处理',
                '文件存储路径和URL配置'
            ]
        }
    ]
    
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
        'personal_tags': personal_tags,
        'learning_journey': learning_journey,
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