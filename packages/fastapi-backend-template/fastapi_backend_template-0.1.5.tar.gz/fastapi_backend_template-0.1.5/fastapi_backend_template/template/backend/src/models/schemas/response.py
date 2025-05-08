from enum import Enum
import typing

from src.models.schemas.base import BaseSchemaModel


class ResponseStatus(str, Enum):
    """API响应状态枚举"""
    SUCCESS = "success"
    ERROR = "error"


class BaseResponse(BaseSchemaModel):
    """API基础响应模型"""
    status: ResponseStatus
    code: int
    message: str


class DataResponse(BaseResponse):
    """包含数据的API响应模型"""
    data: typing.Any = None


def success_response(*, data: typing.Any = None, code: int = 200, message: str = "Operation successful") -> DataResponse:
    """
    创建成功响应
    
    Args:
        data: 响应数据
        code: HTTP状态码
        message: 成功消息
    
    Returns:
        标准格式的成功响应
    """
    return DataResponse(
        status=ResponseStatus.SUCCESS,
        code=code,
        message=message,
        data=data
    )


def error_response(*, code: int = 400, message: str = "Operation failed") -> BaseResponse:
    """
    创建错误响应
    
    Args:
        code: HTTP错误码
        message: 错误消息
    
    Returns:
        标准格式的错误响应
    """
    return BaseResponse(
        status=ResponseStatus.ERROR,
        code=code,
        message=message
    )


# 常用错误响应
VALIDATION_ERROR = error_response(code=422, message="Validation error")
UNAUTHORIZED_ERROR = error_response(code=401, message="Unauthorized")
FORBIDDEN_ERROR = error_response(code=403, message="Forbidden")
NOT_FOUND_ERROR = error_response(code=404, message="Resource not found")
INTERNAL_SERVER_ERROR = error_response(code=500, message="Internal server error") 