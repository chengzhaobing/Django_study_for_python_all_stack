from django.shortcuts import render
import os
from django.conf import settings

def learning_summary(request):
    """学习总结页面视图"""
    
    # 笔记记录目录路径
    notes_path = os.path.join(settings.BASE_DIR, '笔记记录')
    
    # 统计数据
    total_categories = 6  # Django学习笔记、Form组件、Ajax、前端图表、文件操作、浏览器-网站
    total_files = 0
    total_images = 0
    total_code_files = 0
    
    # 学习分类数据
    learning_categories = [
        {
            'name': 'Django学习笔记',
            'slug': 'django',
            'icon': 'fas fa-code',
            'description': 'Django框架核心概念、模板语法、URL配置、视图处理等基础知识学习',
            'files': [
                {
                    'name': '图标使用.md',
                    'icon': 'fas fa-icons',
                    'description': 'FontAwesome图标库的使用方法和最佳实践'
                },
                {
                    'name': 'Django模板语法注意事项(重点).md',
                    'icon': 'fas fa-file-code',
                    'description': '模板语法核心要点：对象属性访问、date过滤器、choices动态渲染'
                },
                {
                    'name': 'Django中的搜索与查询方法.md',
                    'icon': 'fas fa-search',
                    'description': 'ORM查询优化、搜索功能实现和数据库操作技巧'
                },
                {
                    'name': '两种url传参方式.md',
                    'icon': 'fas fa-link',
                    'description': 'URL参数传递的不同方式和应用场景分析'
                },
                {
                    'name': '中间件.md',
                    'icon': 'fas fa-layer-group',
                    'description': 'Django中间件机制、自定义中间件开发和应用'
                },
                {
                    'name': '时间插件使用方法.md',
                    'icon': 'fas fa-clock',
                    'description': '日期时间组件集成和时间格式化处理'
                }
            ]
        },
        {
            'name': 'Form组件和ModelForm组件',
            'slug': 'form',
            'icon': 'fas fa-wpforms',
            'description': 'Django表单组件的使用、验证机制、样式定制和ModelForm的高级应用',
            'files': [
                {
                    'name': '初始Form组件.md',
                    'icon': 'fas fa-file-alt',
                    'description': 'Form组件基础概念和基本使用方法'
                },
                {
                    'name': '初始ModelForm组件.md',
                    'icon': 'fas fa-database',
                    'description': 'ModelForm组件与模型的关联和字段映射'
                },
                {
                    'name': 'ModelForm组件使用.md',
                    'icon': 'fas fa-cogs',
                    'description': 'ModelForm高级用法和实际项目应用'
                },
                {
                    'name': 'ModelForm组件之钩子方法.md',
                    'icon': 'fas fa-hook',
                    'description': '表单验证钩子方法和自定义验证逻辑'
                },
                {
                    'name': '搜索方法.md',
                    'icon': 'fas fa-filter',
                    'description': '表单搜索功能实现和查询优化技巧'
                }
            ]
        },
        {
            'name': 'Ajax异步交互',
            'slug': 'ajax',
            'icon': 'fas fa-exchange-alt',
            'description': 'Ajax技术在Django中的应用、异步数据交互、错误处理和用户体验优化',
            'files': [
                {
                    'name': '模态框实现方法.md',
                    'icon': 'fas fa-window-restore',
                    'description': 'Bootstrap模态框与Ajax结合的动态交互实现'
                },
                {
                    'name': 'Ajax实现错误信息.md',
                    'icon': 'fas fa-exclamation-triangle',
                    'description': 'Ajax错误处理机制和用户友好的错误信息展示'
                },
                {
                    'name': 'Ajax实现删除.md',
                    'icon': 'fas fa-trash-alt',
                    'description': '无刷新删除功能和确认对话框的实现'
                },
                {
                    'name': '后端数据库数据获取传给前端.md',
                    'icon': 'fas fa-server',
                    'description': '后端数据序列化和前端数据渲染的完整流程'
                }
            ]
        },
        {
            'name': '前端图表',
            'slug': 'chart',
            'icon': 'fas fa-chart-bar',
            'description': '数据可视化技术、Chart.js和Highcharts图表库的集成与应用',
            'files': [
                {
                    'name': '图表.md',
                    'icon': 'fas fa-chart-line',
                    'description': '多种图表类型的实现和数据可视化最佳实践'
                }
            ]
        },
        {
            'name': '文件操作',
            'slug': 'file',
            'icon': 'fas fa-file-upload',
            'description': '文件上传、下载、处理和存储的完整解决方案',
            'files': [
                {
                    'name': '上传文件.md',
                    'icon': 'fas fa-cloud-upload-alt',
                    'description': '文件上传功能实现、文件类型验证和安全处理'
                }
            ]
        },
        {
            'name': '浏览器-网站交互',
            'slug': 'browser',
            'icon': 'fas fa-globe',
            'description': '浏览器与服务器交互机制、Session管理、验证码生成和安全策略',
            'files': [
                {
                    'name': '浏览器访问特点.md',
                    'icon': 'fas fa-browser',
                    'description': 'HTTP协议和浏览器请求响应机制分析'
                },
                {
                    'name': '浏览器与网站.md',
                    'icon': 'fas fa-network-wired',
                    'description': '客户端与服务端通信原理和数据传输'
                },
                {
                    'name': 'Django支持的Session写入.md',
                    'icon': 'fas fa-key',
                    'description': 'Session机制和用户状态管理实现'
                },
                {
                    'name': '图片验证码.md',
                    'icon': 'fas fa-shield-alt',
                    'description': 'Pillow库验证码生成和安全验证机制'
                },
                {
                    'name': 'Ajax请求.md',
                    'icon': 'fas fa-paper-plane',
                    'description': 'Ajax请求处理和异步通信优化'
                }
            ]
        }
    ]
    
    # 计算文件统计
    for category in learning_categories:
        total_files += len(category['files'])
    
    # 估算图片和代码文件数量（基于实际目录结构）
    total_images = 25  # 各目录中的img.png, img_1.png等
    total_code_files = 8  # .py文件和其他代码文件
    
    # 学习进度数据
    learning_progress = [
        {'name': 'Django基础', 'percentage': 95, 'color': '#28a745'},
        {'name': 'Form组件', 'percentage': 90, 'color': '#007bff'},
        {'name': 'Ajax交互', 'percentage': 85, 'color': '#ffc107'},
        {'name': '数据可视化', 'percentage': 80, 'color': '#dc3545'},
        {'name': '文件操作', 'percentage': 75, 'color': '#6f42c1'},
        {'name': '浏览器交互', 'percentage': 88, 'color': '#fd7e14'},
    ]
    
    context = {
        'total_categories': total_categories,
        'total_files': total_files,
        'total_images': total_images,
        'total_code_files': total_code_files,
        'study_days': 45,  # 估算学习天数
        'completion_rate': 87,  # 整体完成度
        'learning_categories': learning_categories,
        'learning_progress': learning_progress,
    }
    
    return render(request, 'learning_summary.html', context)

def code_guide(request):
    """代码说明页面视图"""
    
    context = {
        'page_title': '代码说明与开发指南',
        'description': 'Django全栈开发技术栈详解与最佳实践',
    }
    
    return render(request, 'code_guide.html', context)