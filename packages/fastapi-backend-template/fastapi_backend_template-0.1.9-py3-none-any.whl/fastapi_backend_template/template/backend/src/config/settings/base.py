import logging
import pathlib
from typing import Dict, Any

import pydantic
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

# 计算backend目录的父目录（.env所在位置）
ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.resolve().parent


class BackendBaseSettings(BaseSettings):
    TITLE: str = "DAPSQL FARN-Stack Template Application"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = False

    # 服务器配置
    SERVER_HOST: str = Field(default="0.0.0.0", validation_alias="BACKEND_SERVER_HOST")
    SERVER_PORT: int = Field(default=8000, validation_alias="BACKEND_SERVER_PORT")  
    SERVER_WORKERS: int = Field(default=1, validation_alias="BACKEND_SERVER_WORKERS")
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    # MySQL 数据库配置
    DB_MYSQL_HOST: str = Field(default="localhost", validation_alias="MYSQL_HOST")
    DB_MYSQL_NAME: str = Field(default="fastapi_db", validation_alias="MYSQL_DB")
    DB_MYSQL_PASSWORD: str = Field(default="password", validation_alias="MYSQL_PASSWORD")
    DB_MYSQL_PORT: int = Field(default=3306, validation_alias="MYSQL_PORT")
    DB_MYSQL_USERNAME: str = Field(default="root", validation_alias="MYSQL_USERNAME")
    
    # 数据库连接池配置
    DB_MAX_POOL_CON: int = Field(default=20)
    DB_POOL_SIZE: int = Field(default=5)
    DB_POOL_OVERFLOW: int = Field(default=10)
    DB_TIMEOUT: int = Field(default=30)

    IS_DB_ECHO_LOG: bool = Field(default=True)
    IS_DB_FORCE_ROLLBACK: bool = Field(default=False)
    IS_DB_EXPIRE_ON_COMMIT: bool = Field(default=False)

    # JWT和身份认证配置
    API_TOKEN: str = Field(default="api_token")
    AUTH_TOKEN: str = Field(default="auth_token")
    JWT_TOKEN_PREFIX: str = Field(default="Bearer")
    JWT_SECRET_KEY: str = Field(default="secret_key")
    JWT_SUBJECT: str = Field(default="access")
    JWT_MIN: int = Field(default=60)
    JWT_HOUR: int = Field(default=24)
    JWT_DAY: int = Field(default=30)
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = 0  # 将在模型验证中计算

    # CORS配置
    IS_ALLOWED_CREDENTIALS: bool = Field(default=True)
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # React default port
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000",  # React docker port
        "http://127.0.0.1:3001",
        "http://localhost:5173",  # Qwik default port
        "http://0.0.0.0:5173",
        "http://127.0.0.1:5173",  # Qwik docker port
        "http://127.0.0.1:5174",
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    # 日志配置
    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    # 安全配置
    HASHING_ALGORITHM_LAYER_1: str = Field(default="bcrypt")
    HASHING_ALGORITHM_LAYER_2: str = Field(default="argon2")
    HASHING_SALT: str = Field(default="salt")
    JWT_ALGORITHM: str = Field(default="HS256")

    # Pydantic v2兼容的配置
    model_config = {
        "case_sensitive": True,
        "env_file": str(ROOT_DIR / ".env"),
        "env_file_encoding": "utf-8",
        "validate_assignment": True,
        "extra": "allow",  # 允许额外的环境变量
    }
    
    @field_validator("JWT_ACCESS_TOKEN_EXPIRATION_TIME", mode="before")
    def compute_expiration_time(cls, v: int, info) -> int:
        """计算JWT令牌过期时间"""
        values = info.data
        return values.get("JWT_MIN", 60) * values.get("JWT_HOUR", 24) * values.get("JWT_DAY", 30)

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }
