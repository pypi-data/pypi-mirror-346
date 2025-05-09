"""
配置工具模块

提供灵活的配置加载和管理功能，支持从多个配置源读取配置。
"""

import os
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

from pydantic import BaseSettings

# 配置类型变量
T = TypeVar('T', bound=BaseSettings)

logger = logging.getLogger(__name__)


class ConfigLoader:
    """配置加载器
    
    支持从多个配置源加载配置，包括默认值、环境变量、配置文件等。
    
    示例:
        >>> from src.config.settings.base import BackendBaseSettings
        >>> config = ConfigLoader.load_config(BackendBaseSettings)
        >>> print(config.SERVER_HOST)
    """
    
    @staticmethod
    def find_env_file(filename: str = ".env") -> Optional[Path]:
        """
        查找环境变量文件
        
        按以下顺序查找:
        1. 当前工作目录
        2. 项目根目录
        3. backend目录
        
        Args:
            filename: 环境变量文件名，默认为.env
            
        Returns:
            找到的环境变量文件路径，如果未找到则返回None
        """
        # 当前目录
        current_dir = Path.cwd()
        if (current_dir / filename).exists():
            return current_dir / filename
            
        # 项目根目录（向上最多查找3层）
        parent = current_dir
        for _ in range(3):
            if (parent / filename).exists():
                return parent / filename
            parent = parent.parent
            if not parent or parent == parent.parent:
                break
                
        # backend目录
        if (current_dir / "backend" / filename).exists():
            return current_dir / "backend" / filename
            
        return None
    
    @staticmethod
    @lru_cache()
    def load_config(config_class: Type[T], **kwargs) -> T:
        """
        加载配置
        
        Args:
            config_class: 配置类
            **kwargs: 传递给配置类的其他参数
            
        Returns:
            配置实例
        """
        env_file = ConfigLoader.find_env_file()
        env_file_path = str(env_file) if env_file else None
        
        if env_file_path:
            logger.info(f"从 {env_file_path} 加载配置")
            if "env_file" not in kwargs:
                kwargs["env_file"] = env_file_path
        else:
            logger.warning("未找到.env文件，将使用默认值和环境变量")
            
        return config_class(**kwargs)
        
    @staticmethod
    def get_env(key: str, default: Any = None) -> str:
        """
        获取环境变量值
        
        Args:
            key: 环境变量名
            default: 默认值
            
        Returns:
            环境变量值
        """
        return os.environ.get(key, default)
        
    @staticmethod
    def set_env(key: str, value: str) -> None:
        """
        设置环境变量值
        
        Args:
            key: 环境变量名
            value: 环境变量值
        """
        os.environ[key] = value 