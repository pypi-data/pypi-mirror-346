# 脚手架工具使用说明

`scaffold.py` 是一个用于快速创建基于FastAPI-Backend-Template的新项目的脚手架工具。

## 使用方法

### 基本用法

最简单的用法是直接运行脚本，使用默认配置：

```bash
python scaffold.py my-project
```

这将在当前目录下创建一个名为 `my-project` 的新项目。

### 命令行选项

脚手架工具支持以下命令行选项：

```
usage: scaffold.py [-h] [--db-user DB_USER] [--db-password DB_PASSWORD] [--db-name DB_NAME]
                  [--db-host DB_HOST] [--db-port DB_PORT] [--skip-venv] [--output-dir OUTPUT_DIR]
                  [project_name]

FastAPI Backend Template 脚手架工具

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

### 示例

1. 创建自定义数据库配置的项目：

```bash
python scaffold.py my-project --db-user myuser --db-password mypass --db-name custom_db
```

2. 指定输出目录：

```bash
python scaffold.py --output-dir /path/to/projects/my-project
```

3. 跳过虚拟环境创建：

```bash
python scaffold.py my-project --skip-venv
```

## 脚手架工具功能

脚手架工具执行以下操作：

1. 复制模板文件到新的项目目录
2. 更新项目名称和相关配置
3. 创建包含随机生成密钥的`.env`配置文件
4. 生成`README.md`文件
5. 创建虚拟环境并安装依赖(除非指定`--skip-venv`)

## 项目结构

创建的项目具有以下结构：

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
└── venv/               # 虚拟环境 (如果未指定--skip-venv)
```

## 使用创建的项目

1. 进入项目目录：
   ```bash
   cd my-project
   ```

2. 激活虚拟环境：
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. 启动服务：
   ```bash
   cd backend
   python app.py
   ```

4. 访问API文档：[http://localhost:8000/docs](http://localhost:8000/docs) 