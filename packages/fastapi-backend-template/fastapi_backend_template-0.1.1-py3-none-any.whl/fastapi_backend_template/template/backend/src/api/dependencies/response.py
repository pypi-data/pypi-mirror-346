from fastapi import Depends, Response
import typing

from src.models.schemas.response import DataResponse
from src.utilities.formatters.response_formatter import ResponseFormatter


def format_response(status_code: int = 200, message: str = "Operation successful"):
    """
    响应格式化依赖，用于路由函数
    
    Args:
        status_code: 默认HTTP状态码
        message: 默认成功消息
        
    Returns:
        格式化响应的依赖函数
    """
    def dependency(response: Response) -> typing.Callable[[typing.Any], DataResponse]:
        def formatter(data: typing.Any) -> DataResponse:
            # 设置实际HTTP状态码
            response.status_code = status_code
            return ResponseFormatter.format_response(data, status_code, message)
        return formatter
    return Depends(dependency)


# 预定义常用响应依赖
format_200_response = format_response(status_code=200, message="Operation successful")
format_201_response = format_response(status_code=201, message="Resource created successfully")
format_202_response = format_response(status_code=202, message="Request accepted for processing")
format_204_response = format_response(status_code=204, message="No content") 