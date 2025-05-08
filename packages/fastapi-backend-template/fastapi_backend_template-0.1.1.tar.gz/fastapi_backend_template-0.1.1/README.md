# FastAPI Backend Template

![PyPI Version](https://img.shields.io/pypi/v/fastapi-backend-template)
![Python Version](https://img.shields.io/pypi/pyversions/fastapi-backend-template)
![License](https://img.shields.io/pypi/l/fastapi-backend-template)

快速创建基于FastAPI的后端项目的脚手架工具，提供完整的项目结构和最佳实践。

## 特性

- 🚀 完整的FastAPI项目结构
- 🔐 内置JWT认证和密码哈希实现
- 🗃️ SQLAlchemy ORM数据库集成（支持MySQL）
- 📊 统一的API响应格式
- 🛠️ 易于配置的环境变量
- 📝 自动生成API文档
- 🧪 测试框架集成
- 🐳 Docker支持
- 🔄 数据库迁移工具(Alembic)
- ⚡ 异步数据库会话管理

## 安装

```bash
pip install fastapi-backend-template
```

## 快速开始

### 创建新项目

```bash
# 基本用法
fastapi-backend my-project

# 自定义数据库配置
fastapi-backend my-project --db-user myuser --db-password mypass --db-name custom_db
```

### 启动项目

```bash
cd my-project
# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

cd backend
python app.py
```

访问API文档: http://localhost:8000/docs

## 命令行选项

```
usage: fastapi-backend [-h] [--db-user DB_USER] [--db-password DB_PASSWORD]
                      [--db-name DB_NAME] [--db-host DB_HOST] [--db-port DB_PORT]
                      [--skip-venv] [--output-dir OUTPUT_DIR]
                      [project_name]

位置参数:
  project_name          项目名称 (默认: fastapi-backend)

可选参数:
  -h, --help            显示帮助信息并退出
  --db-user DB_USER     数据库用户名 (默认: root)
  --db-password DB_PASSWORD
                        数据库密码 (默认: password)
  --db-name DB_NAME     数据库名称 (默认: 项目名称转换为下划线形式)
  --db-host DB_HOST     数据库主机 (默认: localhost)
  --db-port DB_PORT     数据库端口 (默认: 3306)
  --skip-venv           跳过创建虚拟环境和安装依赖
  --output-dir OUTPUT_DIR
                        输出目录 (默认: 当前目录下以项目名称命名的文件夹)
```

## 项目结构

```
my-project/
├── .env                # 环境变量配置
├── README.md           # 项目文档
├── backend/            # 后端代码
│   ├── app.py          # 应用入口点
│   ├── requirements.txt# 依赖列表
│   ├── Dockerfile      # Docker配置
│   ├── entrypoint.sh   # Docker入口脚本
│   ├── alembic.ini     # 数据库迁移配置
│   └── src/            # 源代码
│       ├── api/                    # API路由与控制器
│       │   ├── dependencies/       # API依赖项(会话、仓库等)
│       │   ├── routes/             # 路由定义
│       │   └── endpoints.py        # API端点注册
│       ├── config/                 # 配置
│       │   ├── settings/           # 环境设置(开发、生产等)
│       │   ├── events.py           # 应用事件处理
│       │   └── manager.py          # 配置管理器
│       ├── models/                 # 数据模型
│       │   ├── db/                 # 数据库模型
│       │   └── schemas/            # Pydantic模式
│       ├── repository/             # 数据库交互
│       │   ├── crud/               # CRUD操作
│       │   ├── migrations/         # 数据库迁移脚本
│       │   ├── database.py         # 数据库连接
│       │   └── base.py             # 基础仓库类
│       ├── securities/             # 安全相关
│       │   ├── authorizations/     # 授权
│       │   ├── hashing/            # 密码哈希
│       │   └── verifications/      # 凭证验证
│       └── utilities/              # 工具函数
│           ├── exceptions/         # 异常定义
│           ├── formatters/         # 格式化工具
│           └── messages/           # 消息定义
└── venv/               # 虚拟环境
```

## 主要功能详解

### 统一的API响应格式

所有API响应都遵循统一的JSON格式：

```json
{
  "status": "success",
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

### 异常处理

内置全局异常处理器，自动将异常转换为统一的API响应格式。

### 认证系统

- JWT令牌认证
- 密码双重哈希(bcrypt + argon2)
- 可配置的令牌过期时间

### 数据库会话管理

- 每个请求自动创建和关闭会话
- 异步会话支持
- 事务管理

### 环境配置

易于管理的环境变量，支持不同环境(开发、测试、生产)的配置。

## 常见问题(FAQ)

### 如何添加新的API路由?

在`src/api/routes/`目录下创建新的路由文件，然后在`src/api/endpoints.py`中注册。

### 如何修改数据库连接?

编辑项目根目录下的`.env`文件，更新数据库配置。

### 如何运行数据库迁移?

```bash
cd backend
alembic upgrade head  # 应用所有迁移
alembic revision --autogenerate -m "描述"  # 创建新迁移
```

### 如何使用Docker运行?

```bash
cd my-project
docker-compose up -d
```

## 配置为PyPI包

如果您想发布此包到PyPI，请按照以下步骤操作：

1. 更新`setup.py`中的作者信息和URL
2. 确保所有模板文件已复制到`fastapi_backend_template/template`目录
3. 构建包并上传到PyPI：

```bash
# 安装构建工具
pip install build twine

# 构建包
python -m build

# 上传到PyPI测试服务器
twine upload --repository testpypi dist/*

# 上传到正式PyPI
twine upload dist/*
```

## 贡献指南

欢迎贡献代码、报告问题或提供改进建议。请遵循以下步骤：

1. Fork此仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 许可证

MIT

---
