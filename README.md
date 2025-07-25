# Django员工管理系统 - 全栈开发学习项目

一个基于Django框架的现代化员工管理系统，提供完整的员工信息管理、部门管理、任务管理等功能。这是一个全栈开发学习项目，展示了Django框架的核心特性和最佳实践。

## 🚀 项目特色

- 🎨 **现代化UI设计** - 采用Bootstrap 5框架，具有美观的响应式界面
- 🔐 **完整的用户认证** - 登录、注册、忘记密码，集成图片验证码防护
- 📊 **数据可视化** - 集成Chart.js和Highcharts，支持多种图表类型
- 📱 **响应式设计** - 完美适配PC、平板、手机等各种设备
- ✨ **粒子背景效果** - 登录页面具有动态粒子背景，提升视觉体验
- 🔄 **Ajax异步交互** - 无刷新操作，提升用户体验
- 📁 **文件处理功能** - Excel导入导出，文件上传下载
- 🏷️ **个人标签系统** - 展示个人技能和特长
- 📚 **学习历程记录** - 完整的学习笔记和经验总结

## 📋 功能模块

### 🔐 用户认证系统
- **用户登录** - 支持用户名密码登录，集成图片验证码
- **用户注册** - 新用户注册功能，包含表单验证
- **忘记密码** - 密码重置功能，通过用户名重置
- **图片验证码** - 支持数字、字母、混合三种模式，可配置切换
- **自动刷新验证码** - 验证失败时自动刷新验证码

### 👥 员工管理
- **员工信息管理** - 员工信息的完整CRUD操作
- **高级搜索** - 支持按部门、姓名等条件搜索
- **批量操作** - Excel批量导入导出功能
- **头像管理** - 员工头像上传和管理

### 🏢 部门管理
- **部门信息管理** - 部门的增删改查操作
- **层级关系** - 部门层级结构展示
- **员工统计** - 各部门员工数量统计

### 📋 任务管理
- **任务创建** - 创建和分配任务
- **进度跟踪** - 任务状态和进度管理
- **优先级设置** - 任务优先级分类
- **状态管理** - 待处理、进行中、已完成状态

### 📦 订单管理
- **订单信息** - 订单的完整生命周期管理
- **状态跟踪** - 订单状态实时更新
- **数据统计** - 订单数据分析和报表

### 📊 数据可视化
- **员工统计图表** - 员工分布和统计信息
- **部门分析** - 部门数据饼状图展示
- **任务进度** - 任务完成情况折线图
- **实时更新** - 数据实时刷新和更新

### 📁 文件操作
- **文件上传** - 支持多种文件格式上传
- **Excel处理** - Excel文件的读取和写入
- **批量导入** - 员工信息批量导入功能
- **数据导出** - 支持数据导出为Excel格式

### 👤 个人中心
- **个人资料** - 用户个人信息展示和编辑
- **我的信息** - 技术栈展示、项目经验和代码示例
- **个人标签** - 展示个人技能和特长标签
- **学习历程** - 完整的学习笔记和经验总结

## 🛠️ 技术栈

### 后端技术
- **Python 3.x** - 主要开发语言
- **Django 4.2.23** - Web开发框架
- **MySQL** - 关系型数据库（支持SQLite3开发）
- **Redis** - 缓存和Session存储（可选）
- **Pillow** - 图像处理库，用于验证码生成
- **openpyxl** - Excel文件处理库

### 前端技术
- **HTML5/CSS3** - 页面结构和样式
- **JavaScript/jQuery** - 前端交互逻辑
- **Bootstrap 5** - 响应式UI框架
- **Font Awesome** - 图标库
- **Chart.js/Highcharts** - 数据可视化图表库
- **Particles.js** - 粒子背景特效

### 开发工具
- **PyCharm** - 集成开发环境
- **Git** - 版本控制系统
- **Chrome DevTools** - 前端调试工具

## 📁 项目结构

```
dya2/
├── app02/                      # 主应用目录
│   ├── migrations/             # 数据库迁移文件
│   ├── static/                 # 静态资源
│   │   ├── css/               # 样式文件
│   │   ├── js/                # JavaScript文件
│   │   ├── img/               # 图片资源
│   │   └── plugins/           # 第三方插件
│   ├── templates/             # 模板文件
│   │   ├── login.html         # 登录页面
│   │   ├── register.html      # 注册页面
│   │   ├── forgot_password.html # 忘记密码页面
│   │   ├── layout.html        # 基础布局模板
│   │   ├── my_info.html       # 个人信息页面
│   │   └── ...                # 其他页面模板
│   ├── utils/                 # 工具模块
│   │   ├── bootstrap.py       # Bootstrap样式类
│   │   ├── code.py            # 验证码生成
│   │   └── pagination.py     # 分页组件
│   ├── views/                 # 视图模块
│   │   ├── account.py         # 账户相关视图
│   │   ├── depart.py          # 部门管理视图
│   │   ├── user.py            # 用户管理视图
│   │   ├── task.py            # 任务管理视图
│   │   ├── order.py           # 订单管理视图
│   │   ├── chart.py           # 图表数据视图
│   │   ├── upload.py          # 文件上传视图
│   │   └── profile.py         # 个人信息视图
│   ├── models.py              # 数据模型
│   └── admin.py               # 管理后台配置
├── dya2/                      # 项目配置目录
│   ├── settings.py            # 项目设置
│   ├── urls.py                # URL路由配置
│   └── wsgi.py                # WSGI配置
├── 笔记记录/                   # 学习笔记目录
│   ├── Django学习笔记/        # Django相关笔记
│   ├── Form组件和ModelForm组件/ # Form组件学习笔记
│   ├── ajax/                  # Ajax技术笔记
│   ├── 前端图表/               # 图表技术笔记
│   ├── 文件操作/               # 文件处理笔记
│   └── 浏览器网站交互/         # 浏览器交互笔记
├── media/                     # 媒体文件目录
├── static/                    # 静态文件收集目录
├── manage.py                  # Django管理脚本
├── requirements.txt           # 项目依赖
└── README.md                  # 项目说明文档
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ (开发环境可使用SQLite3)
- Redis (可选，用于缓存)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/dya2.git
cd dya2
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置数据库**
- 创建MySQL数据库（生产环境）
- 修改 `dya2/settings.py` 中的数据库配置

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. **执行数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **创建超级用户**
```bash
python manage.py createsuperuser
```

7. **运行项目**
```bash
python manage.py runserver
```

8. **访问应用**
- 前台地址：http://127.0.0.1:8000/
- 管理后台：http://127.0.0.1:8000/admin/

## 🌐 页面导航

### 认证页面
- **用户登录**: http://127.0.0.1:8000/login/
- **用户注册**: http://127.0.0.1:8000/register/
- **忘记密码**: http://127.0.0.1:8000/forgot-password/
- **验证码**: http://127.0.0.1:8000/image/code/

### 管理页面
- **首页**: http://127.0.0.1:8000/
- **用户管理**: http://127.0.0.1:8000/user/list/
- **部门管理**: http://127.0.0.1:8000/depart/list/
- **管理员**: http://127.0.0.1:8000/admin/list/
- **任务管理**: http://127.0.0.1:8000/task/list/
- **订单管理**: http://127.0.0.1:8000/order/list/

### 功能页面
- **数据图表**: http://127.0.0.1:8000/chart/list/
- **文件上传**: http://127.0.0.1:8000/upload/list/
- **个人资料**: http://127.0.0.1:8000/profile/
- **我的信息**: http://127.0.0.1:8000/my-info/

### 管理后台
- **Django Admin**: http://127.0.0.1:8000/admin/

## 📖 学习要点

本项目涵盖了Django全栈开发的核心知识点和最佳实践：

### 1. Django框架核心
- **MTV架构模式** - Model-Template-View设计模式
- **URL路由系统** - URL配置和参数传递
- **视图函数** - 函数视图和类视图的使用
- **模板系统** - Django模板语法和继承
- **ORM操作** - 数据库查询和关系处理

### 2. Form组件应用
- **Form组件** - 表单验证和数据清洗
- **ModelForm** - 基于Model的表单自动生成
- **钩子方法** - 自定义验证逻辑
- **样式类** - Bootstrap样式集成
- **错误处理** - 表单错误信息展示

### 3. Ajax异步交互
- **jQuery Ajax** - 前后端异步通信
- **JSON数据** - 数据序列化和传输
- **模态框** - 弹窗交互实现
- **错误处理** - Ajax错误信息显示
- **CSRF保护** - 跨站请求伪造防护

### 4. 用户认证系统
- **Session管理** - 会话状态保持
- **Cookie机制** - 客户端数据存储
- **图片验证码** - Pillow库验证码生成
- **密码加密** - 用户密码安全处理
- **权限控制** - 用户访问权限管理

### 5. 数据可视化
- **Chart.js** - 轻量级图表库
- **Highcharts** - 专业图表解决方案
- **数据统计** - 后端数据聚合查询
- **实时更新** - Ajax动态数据刷新
- **响应式图表** - 适配不同屏幕尺寸

### 6. 文件操作技术
- **文件上传** - Django文件处理机制
- **Excel处理** - openpyxl库应用
- **批量导入** - 数据批量处理
- **文件验证** - 文件类型和大小检查
- **存储配置** - 媒体文件管理

### 7. 前端技术集成
- **Bootstrap 5** - 响应式UI框架
- **JavaScript/jQuery** - 前端交互逻辑
- **Particles.js** - 粒子背景特效
- **Font Awesome** - 图标库使用
- **CSS3动画** - 页面动效实现

## 🔧 配置说明

### 验证码配置
在 `app02/utils/code.py` 中可以配置验证码类型：

```python
# 数字验证码
mode = 1  # 纯数字

# 字母验证码  
mode = 2  # 纯字母

# 混合验证码
mode = 3  # 数字+字母
```

### Session配置
在 `settings.py` 中可以配置Session存储方式：

```python
# 数据库存储（默认）
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# 缓存存储
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# 文件存储
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
```

## 📚 学习资源

项目包含完整的学习笔记，位于 `笔记记录/` 目录：

- **Django学习笔记** - Django框架核心概念和应用
- **Form组件笔记** - Form和ModelForm组件深入应用
- **Ajax技术笔记** - 前后端异步交互实现
- **图表技术笔记** - 数据可视化实现方法
- **文件操作笔记** - 文件上传下载和Excel处理
- **浏览器交互笔记** - HTTP协议和Session机制

每个笔记都包含详细的代码示例和实践经验，是学习Django全栈开发的宝贵资源。

## 🤝 贡献指南

欢迎为这个项目做出贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目地址：[https://github.com/yourusername/dya2](https://github.com/yourusername/dya2)
- 问题反馈：[Issues](https://github.com/yourusername/dya2/issues)

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和提供技术支持的开源社区。

---

**注意**：这是一个学习项目，主要用于Django框架的学习和实践。如果用于生产环境，请确保进行充分的安全性测试和性能优化。