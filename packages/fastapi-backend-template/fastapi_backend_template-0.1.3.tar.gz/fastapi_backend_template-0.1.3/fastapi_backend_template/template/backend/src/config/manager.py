"""
配置管理器模块

处理不同环境的配置加载和管理。
"""

from functools import lru_cache

from src.config.settings.base import BackendBaseSettings
from src.config.settings.development import BackendDevSettings
from src.config.settings.environment import Environment
from src.config.settings.production import BackendProdSettings
from src.config.settings.staging import BackendStageSettings
from src.config.utils import ConfigLoader


class BackendSettingsFactory:
    """后端设置工厂
    
    根据当前环境返回相应的配置实例。
    """
    
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> BackendBaseSettings:
        """获取当前环境的配置实例"""
        if self.environment == Environment.DEVELOPMENT.value:
            return ConfigLoader.load_config(BackendDevSettings)
        elif self.environment == Environment.STAGING.value:
            return ConfigLoader.load_config(BackendStageSettings)
        return ConfigLoader.load_config(BackendProdSettings)


@lru_cache()
def get_settings() -> BackendBaseSettings:
    """获取当前环境的配置，并缓存结果
    
    Returns:
        当前环境的配置实例
    """
    environment = ConfigLoader.get_env("ENVIRONMENT", default="DEV")
    return BackendSettingsFactory(environment=environment)()


# 导出全局配置实例
settings: BackendBaseSettings = get_settings()
