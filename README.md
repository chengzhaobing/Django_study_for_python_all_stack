# Django Study for Python Full Stack

一个基于Django框架的全栈开发学习项目，包含用户管理、部门管理、任务管理、订单管理等功能模块。

## 项目特色

- 🎨 **美观的UI设计** - 采用Bootstrap框架，具有现代化的界面设计
- 🔐 **完整的用户认证** - 包含登录、注销、权限管理等功能
- 📊 **数据可视化** - 集成图表展示，支持数据统计分析
- 📱 **响应式设计** - 适配各种设备屏幕尺寸
- ✨ **粒子背景效果** - 登录页面具有动态粒子背景

## 功能模块

### 核心功能
- **用户管理** - 员工信息的增删改查
- **部门管理** - 部门信息管理
- **管理员系统** - 管理员账户管理
- **任务管理** - 任务分配与跟踪
- **订单管理** - 订单信息处理
- **文件上传** - 支持文件上传功能
- **数据统计** - 图表展示和数据分析

### 新增页面
- **个人资料** - 展示用户个人信息和统计数据
- **我的信息** - 技术栈展示、项目经验和代码示例

## 技术栈

- **后端**: Django 4.2.23
- **前端**: Bootstrap 5, HTML5, CSS3, JavaScript
- **数据库**: SQLite3
- **特效**: Particles.js (粒子背景效果)
- **图表**: Chart.js / Highcharts

## 项目结构

```
dya2/
├── app02/                  # 主应用目录
│   ├── migrations/         # 数据库迁移文件
│   ├── static/            # 静态文件
│   │   ├── css/           # 样式文件
│   │   ├── js/            # JavaScript文件
│   │   └── plugins/       # 第三方插件
│   ├── templates/         # 模板文件
│   ├── utils/             # 工具模块
│   ├── views/             # 视图函数
│   └── models.py          # 数据模型
├── dya2/                  # 项目配置目录
├── media/                 # 媒体文件
├── static/                # 静态文件收集目录
├── manage.py              # Django管理脚本
└── requirements.txt       # 依赖包列表
```

## 安装与运行

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/Django_study_for_python_all_stack.git
cd Django_study_for_python_all_stack
```

### 2. 创建虚拟环境
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

### 6. 运行开发服务器
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 查看项目

## 页面预览

- **首页**: http://127.0.0.1:8000/
- **用户登录**: http://127.0.0.1:8000/login/
- **用户管理**: http://127.0.0.1:8000/user/list/
- **部门管理**: http://127.0.0.1:8000/depart/list/
- **个人资料**: http://127.0.0.1:8000/profile/
- **我的信息**: http://127.0.0.1:8000/my-info/

## 学习要点

本项目涵盖了Django全栈开发的核心知识点：

1. **Django基础**
   - MTV架构模式
   - URL路由配置
   - 视图函数编写
   - 模板系统使用

2. **数据库操作**
   - Model定义
   - ORM查询
   - 数据库迁移
   - 外键关系

3. **前端集成**
   - 静态文件管理
   - Bootstrap框架
   - JavaScript交互
   - AJAX请求

4. **用户认证**
   - 登录/注销
   - 会话管理
   - 权限控制

5. **文件处理**
   - 文件上传
   - 图片验证码
   - 静态文件服务

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License