# FastAPI Backend Template

![PyPI Version](https://img.shields.io/pypi/v/fastapi-backend-template)
![Python Version](https://img.shields.io/pypi/pyversions/fastapi-backend-template)
![License](https://img.shields.io/pypi/l/fastapi-backend-template)

快速创建基于FastAPI的后端项目的脚手架工具，提供完整的项目结构和最佳实践。

## 特性

- 🚀 完整的FastAPI项目结构
- 🔐 内置JWT认证和密码哈希实现
- 🗃️ SQLAlchemy ORM数据库集成
- 📊 统一的API响应格式
- 🛠️ 易于配置的环境变量
- 📝 自动生成API文档

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
│   └── src/            # 源代码
│       ├── api/        # API路由与控制器
│       ├── config/     # 配置
│       ├── models/     # 数据模型
│       ├── repository/ # 数据库交互
│       ├── securities/ # 安全相关
│       └── utilities/  # 工具函数
└── venv/               # 虚拟环境
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

## 详细文档

更多详细信息，请参阅[完整文档](https://github.com/yourusername/fastapi-backend-template)。

## 许可证

MIT

---
