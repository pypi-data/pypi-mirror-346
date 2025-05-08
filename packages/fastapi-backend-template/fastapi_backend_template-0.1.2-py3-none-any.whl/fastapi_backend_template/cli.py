#!/usr/bin/env python
"""
FastAPI Backend Template 脚手架工具

用于快速初始化和配置一个新的FastAPI后端项目。
"""

import argparse
import os
import re
import shutil
import secrets
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# 使用importlib.resources替代pkg_resources
try:
    # Python 3.9+
    from importlib.resources import files
except ImportError:
    # Python 3.7-3.8
    try:
        from importlib_resources import files
    except ImportError:
        # 回退到老方法
        import pkg_resources


# 获取包内template目录的路径
def get_template_dir() -> Path:
    """获取模板目录的路径"""
    # 尝试使用importlib.resources
    try:
        try:
            # Python 3.9+
            template_dir = files("fastapi_backend_template").joinpath("template")
            return Path(template_dir)
        except (ImportError, AttributeError):
            # Python 3.7-3.8 使用importlib_resources
            try:
                template_dir = files("fastapi_backend_template").joinpath("template")
                return Path(template_dir)
            except (ImportError, AttributeError):
                pass
    except Exception:
        pass

    # 回退到pkg_resources
    try:
        template_dir = Path(pkg_resources.resource_filename("fastapi_backend_template", "template"))
        # 检查目录是否存在
        if template_dir.exists() and template_dir.is_dir():
            return template_dir
    except (NameError, AttributeError, ImportError, FileNotFoundError):
        pass
    
    # 回退方案：在脚本所在的目录中查找
    module_dir = Path(__file__).resolve().parent
    if (module_dir / "template").exists():
        return module_dir / "template"
        
    # 如果都找不到，再尝试在项目根目录中查找
    project_root = module_dir.parent
    if (project_root / "backend").exists():
        return project_root
        
    # 如果都找不到，抛出错误
    raise FileNotFoundError("无法找到模板目录，请确保包安装正确")


DEFAULT_PROJECT_NAME = "fastapi-backend"
DEFAULT_DB_USER = "root"
DEFAULT_DB_PASSWORD = "password"
DEFAULT_DB_NAME = "fastapi_db"
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = 3306


def generate_secret_key(length=32) -> str:
    """生成随机密钥"""
    return secrets.token_hex(length)


def validate_project_name(name: str) -> str:
    """验证项目名称的有效性"""
    if not re.match(r'^[a-zA-Z][\w-]*$', name):
        raise ValueError(
            "项目名称只能包含字母、数字、下划线和连字符，且必须以字母开头"
        )
    return name


def create_env_file(project_dir: Path, config: Dict[str, Any]) -> None:
    """创建.env文件"""
    env_template = """# 服务器配置
BACKEND_SERVER_HOST=0.0.0.0
BACKEND_SERVER_PORT=8000
BACKEND_SERVER_WORKERS=1

# MySQL 数据库配置
MYSQL_HOST={db_host}
MYSQL_PORT={db_port}
MYSQL_DB={db_name}
MYSQL_USERNAME={db_user}
MYSQL_PASSWORD={db_password}

# 数据库连接池配置
DB_MAX_POOL_CON=20
DB_POOL_SIZE=5
DB_POOL_OVERFLOW=10
DB_TIMEOUT=30
IS_DB_ECHO_LOG=True
IS_DB_FORCE_ROLLBACK=False
IS_DB_EXPIRE_ON_COMMIT=False

# 环境设置
ENVIRONMENT=DEV  # 可选值: DEV, STAGE, PROD

# JWT配置
JWT_TOKEN_PREFIX=Bearer
JWT_SECRET_KEY={jwt_secret}
JWT_SUBJECT=access
JWT_MIN=60
JWT_HOUR=24
JWT_DAY=30
API_TOKEN={api_token}
AUTH_TOKEN={auth_token}

# 跨域资源共享
IS_ALLOWED_CREDENTIALS=True

# 散列算法配置
HASHING_ALGORITHM_LAYER_1=bcrypt
HASHING_ALGORITHM_LAYER_2=argon2
HASHING_SALT={hashing_salt}
JWT_ALGORITHM=HS256
""".format(
        db_host=config["db_host"],
        db_port=config["db_port"],
        db_name=config["db_name"],
        db_user=config["db_user"],
        db_password=config["db_password"],
        jwt_secret=generate_secret_key(32),
        api_token=generate_secret_key(16),
        auth_token=generate_secret_key(16),
        hashing_salt=generate_secret_key(16),
    )
    
    env_path = project_dir / ".env"
    with open(env_path, "w") as f:
        f.write(env_template)
    
    print(f"✅ 已创建环境配置文件: {env_path}")


def create_env_example_file(project_dir: Path, config: Dict[str, Any]) -> None:
    """创建.env.example示例文件"""
    env_example_template = """# 服务器配置
BACKEND_SERVER_HOST=0.0.0.0
BACKEND_SERVER_PORT=8000
BACKEND_SERVER_WORKERS=1

# MySQL 数据库配置
MYSQL_HOST={db_host}
MYSQL_PORT={db_port}
MYSQL_DB={db_name}
MYSQL_USERNAME={db_user}
MYSQL_PASSWORD=your_password_here

# 数据库连接池配置
DB_MAX_POOL_CON=20
DB_POOL_SIZE=5
DB_POOL_OVERFLOW=10
DB_TIMEOUT=30
IS_DB_ECHO_LOG=True
IS_DB_FORCE_ROLLBACK=False
IS_DB_EXPIRE_ON_COMMIT=False

# 环境设置
ENVIRONMENT=DEV  # 可选值: DEV, STAGE, PROD

# JWT配置
JWT_TOKEN_PREFIX=Bearer
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_SUBJECT=access
JWT_MIN=60
JWT_HOUR=24
JWT_DAY=30
API_TOKEN=your_api_token_here
AUTH_TOKEN=your_auth_token_here

# 跨域资源共享
IS_ALLOWED_CREDENTIALS=True

# 散列算法配置
HASHING_ALGORITHM_LAYER_1=bcrypt
HASHING_ALGORITHM_LAYER_2=argon2
HASHING_SALT=your_salt_here
JWT_ALGORITHM=HS256
""".format(
        db_host=config["db_host"],
        db_port=config["db_port"],
        db_name=config["db_name"],
        db_user=config["db_user"]
    )
    
    env_example_path = project_dir / ".env.example"
    with open(env_example_path, "w") as f:
        f.write(env_example_template)
    
    print(f"✅ 已创建环境配置示例文件: {env_example_path}")


def copy_template_files(source_dir: Path, target_dir: Path, exclude: List[str]) -> None:
    """复制模板文件到目标目录"""
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
    
    for item in source_dir.iterdir():
        # 排除指定文件和目录
        if item.name in exclude or item.name.startswith('.'):
            continue
            
        if item.is_dir():
            new_target = target_dir / item.name
            copy_template_files(item, new_target, exclude)
        else:
            shutil.copy2(item, target_dir / item.name)


def update_project_name(project_dir: Path, project_name: str) -> None:
    """更新项目名称相关的配置"""
    settings_file = project_dir / "backend" / "src" / "config" / "settings" / "base.py"
    
    if settings_file.exists():
        with open(settings_file, "r") as f:
            content = f.read()
        
        # 更新应用名称
        content = re.sub(
            r'TITLE: str = ".*?"',
            f'TITLE: str = "{project_name.replace("-", " ").title()}"',
            content
        )
        
        with open(settings_file, "w") as f:
            f.write(content)
            
        print(f"✅ 已更新项目名称: {project_name}")


def setup_virtual_env(project_dir: Path) -> None:
    """设置虚拟环境并安装依赖"""
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", "venv"],
            cwd=project_dir,
            check=True
        )
        
        # 获取激活脚本路径
        if os.name == "nt":  # Windows
            activate_script = project_dir / "venv" / "Scripts" / "activate.bat"
            activate_cmd = str(activate_script)
            pip_cmd = str(project_dir / "venv" / "Scripts" / "pip.exe")
        else:  # Unix/Linux
            activate_script = project_dir / "venv" / "bin" / "activate"
            activate_cmd = f"source {activate_script}"
            pip_cmd = str(project_dir / "venv" / "bin" / "pip")
        
        # 安装依赖
        requirements_file = project_dir / "backend" / "requirements.txt"
        if requirements_file.exists():
            subprocess.run(
                [pip_cmd, "install", "-r", str(requirements_file)],
                cwd=project_dir,
                check=True
            )
            
        print(f"✅ 已创建虚拟环境并安装依赖")
        print(f"   激活虚拟环境: {activate_cmd}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 虚拟环境设置失败: {e}")
        print("   请手动设置虚拟环境并安装依赖:")
        print(f"   python -m venv venv")
        print(f"   {activate_cmd}")
        print(f"   pip install -r backend/requirements.txt")


def create_readme(project_dir: Path, project_name: str) -> None:
    """创建项目README.md文件"""
    readme_content = f"""# {project_name.replace("-", " ").title()}

基于FastAPI构建的后端API服务。

## 项目说明

本项目使用FastAPI-Backend-Template脚手架工具创建，集成了以下功能：

- 🚀 FastAPI框架
- 🔐 JWT认证
- 🗃️ SQLAlchemy ORM数据库集成(MySQL)
- 📊 统一的API响应格式
- 🧪 测试框架
- 🐳 Docker支持
- 🔄 数据库迁移(Alembic)

## 环境设置

1. 创建并激活虚拟环境:
   ```bash
   python -m venv venv
   # Windows
   venv\\Scripts\\activate
   # Linux/Mac
   source venv/bin/activate
   ```

2. 安装依赖:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. 配置环境变量:
   - 已创建默认的`.env`文件，根据需要修改配置

## 数据库初始化

1. 创建数据库:
   ```sql
   CREATE DATABASE {project_name.replace("-", "_")} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. 运行迁移:
   ```bash
   cd backend
   alembic upgrade head
   ```

## 启动服务

```bash
cd backend
python app.py
```

服务将在 http://localhost:8000 运行，API文档在 http://localhost:8000/docs

## 使用Docker

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 项目结构

```
{project_name}/
├── .env                       # 环境变量配置
├── README.md                  # 项目文档
├── backend/                   # 后端代码
    ├── app.py                 # 应用入口点
    ├── requirements.txt       # 依赖列表
    ├── Dockerfile             # Docker配置
    ├── entrypoint.sh          # Docker入口脚本 
    ├── alembic.ini            # 数据库迁移配置
    └── src/                   # 源代码
        ├── api/               # API路由与控制器
        │   ├── dependencies/  # API依赖项(会话、仓库等)
        │   ├── routes/        # 路由定义
        │   └── endpoints.py   # API端点注册
        ├── config/            # 配置
        │   ├── settings/      # 环境设置(开发、生产等)
        │   ├── events.py      # 应用事件处理
        │   └── manager.py     # 配置管理器
        ├── models/            # 数据模型
        │   ├── db/            # 数据库模型
        │   └── schemas/       # Pydantic模式
        ├── repository/        # 数据库交互
        │   ├── crud/          # CRUD操作
        │   ├── migrations/    # 数据库迁移脚本
        │   ├── database.py    # 数据库连接
        │   └── base.py        # 基础仓库类
        ├── securities/        # 安全相关
        │   ├── authorizations/# 授权
        │   ├── hashing/       # 密码哈希
        │   └── verifications/ # 凭证验证
        └── utilities/         # 工具函数
            ├── exceptions/    # 异常定义
            ├── formatters/    # 格式化工具
            └── messages/      # 消息定义
```

## API约定

### 统一的响应格式

所有API响应都遵循统一的JSON格式：

```json
{
  "status": "success", // success, error
  "code": 200,         // HTTP状态码
  "message": "操作成功",  // 响应消息
  "data": { ... }      // 响应数据
}
```

### 认证

API使用JWT令牌认证，调用受保护的API时需要在请求头中包含：

```
Authorization: Bearer your_token_here
```

## 常见任务

### 创建新的API路由

1. 在`src/api/routes/`目录下创建新路由文件
2. 在`src/api/endpoints.py`中注册路由

### 添加新的数据库模型

1. 在`src/models/db/`目录下创建新模型
2. 在`src/repository/crud/`目录下创建对应的CRUD操作

### 运行数据库迁移

```bash
cd backend
# 创建新迁移
alembic revision --autogenerate -m "描述"
# 应用迁移
alembic upgrade head
```

### 运行测试

```bash
cd backend
pytest
```
"""

    readme_path = project_dir / "README.md"
    with open(readme_path, "w") as f:
        f.write(readme_content)
    
    print(f"✅ 已创建README.md文件")


def main():
    parser = argparse.ArgumentParser(description="FastAPI Backend Template 脚手架工具")
    parser.add_argument(
        "project_name",
        nargs="?",
        default=DEFAULT_PROJECT_NAME,
        help=f"项目名称 (默认: {DEFAULT_PROJECT_NAME})"
    )
    parser.add_argument(
        "--db-user", 
        default=DEFAULT_DB_USER,
        help=f"数据库用户名 (默认: {DEFAULT_DB_USER})"
    )
    parser.add_argument(
        "--db-password",
        default=DEFAULT_DB_PASSWORD,
        help=f"数据库密码 (默认: {DEFAULT_DB_PASSWORD})"
    )
    parser.add_argument(
        "--db-name",
        help=f"数据库名称 (默认: 项目名称转换为下划线形式)"
    )
    parser.add_argument(
        "--db-host",
        default=DEFAULT_DB_HOST,
        help=f"数据库主机 (默认: {DEFAULT_DB_HOST})"
    )
    parser.add_argument(
        "--db-port",
        type=int,
        default=DEFAULT_DB_PORT,
        help=f"数据库端口 (默认: {DEFAULT_DB_PORT})"
    )
    parser.add_argument(
        "--skip-venv",
        action="store_true",
        help="跳过创建虚拟环境和安装依赖"
    )
    parser.add_argument(
        "--output-dir",
        help="输出目录 (默认: 当前目录下以项目名称命名的文件夹)"
    )
    
    args = parser.parse_args()
    
    try:
        project_name = validate_project_name(args.project_name)
    except ValueError as e:
        print(f"❌ 错误: {e}")
        return 1
        
    # 数据库名默认为项目名的下划线版本
    db_name = args.db_name or project_name.replace("-", "_").lower()
    
    # 配置输出目录
    output_dir = args.output_dir
    if output_dir:
        project_dir = Path(output_dir).resolve()
    else:
        project_dir = Path.cwd() / project_name
        
    if project_dir.exists() and any(project_dir.iterdir()):
        overwrite = input(f"目录 {project_dir} 已存在且不为空。覆盖现有文件? [y/N]: ").lower()
        if overwrite != 'y':
            print("❌ 操作已取消")
            return 1
    
    # 准备配置
    config = {
        "project_name": project_name,
        "db_user": args.db_user,
        "db_password": args.db_password,
        "db_name": db_name,
        "db_host": args.db_host,
        "db_port": args.db_port,
    }
    
    print(f"🚀 正在创建FastAPI后端项目: {project_name}")
    print(f"   输出目录: {project_dir}")
    
    # 排除不需要复制的文件和目录
    exclude_items = [
        "scaffold.py",
        "venv",
        "__pycache__",
        ".git",
        ".github",
        ".pytest_cache",
        ".vscode",
        ".idea",
    ]
    
    # 获取模板目录
    try:
        template_dir = get_template_dir()
        print(f"模板目录: {template_dir}")
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        return 1
    
    # 复制模板文件
    copy_template_files(template_dir, project_dir, exclude_items)
    print(f"✅ 已复制模板文件到: {project_dir}")
    
    # 更新项目名称
    update_project_name(project_dir, project_name)
    
    # 创建环境配置文件
    create_env_file(project_dir, config)
    
    # 创建环境配置示例文件
    create_env_example_file(project_dir, config)
    
    # 创建README
    create_readme(project_dir, project_name)
    
    # 设置虚拟环境和安装依赖
    if not args.skip_venv:
        setup_virtual_env(project_dir)
    
    print(f"🎉 FastAPI后端项目 {project_name} 已成功创建!")
    print(f"   开始使用:")
    print(f"   cd {project_name}")
    if not args.skip_venv:
        if os.name == "nt":
            print(f"   venv\\Scripts\\activate")
        else:
            print(f"   source venv/bin/activate")
    print(f"   cd backend")
    print(f"   python app.py")
    print(f"   访问API文档: http://localhost:8000/docs")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 