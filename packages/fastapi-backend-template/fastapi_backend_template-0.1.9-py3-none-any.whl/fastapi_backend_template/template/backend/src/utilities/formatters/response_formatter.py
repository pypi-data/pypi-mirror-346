from fastapi import Response
import typing

from src.models.schemas.response import success_response, error_response, DataResponse, BaseResponse


class ResponseFormatter:
    """
    API响应格式化器，用于统一处理API返回格式
    """
    
    @staticmethod
    def format_response(data: typing.Any = None, status_code: int = 200, message: str = "Operation successful") -> DataResponse:
        """
        格式化响应数据
        
        Args:
            data: 原始响应数据
            status_code: HTTP状态码
            message: 操作成功的消息
            
        Returns:
            格式化后的响应对象
        """
        # 如果数据已经是标准响应格式，则直接返回
        if isinstance(data, (BaseResponse, DataResponse)):
            return data
        
        # 创建标准成功响应
        response = success_response(
            data=data, 
            code=status_code,
            message=message
        )
        
        return response
    
    @staticmethod
    def format_create_response(data: typing.Any = None, message: str = "Resource created successfully") -> DataResponse:
        """格式化创建资源的成功响应"""
        return ResponseFormatter.format_response(data, 201, message)
    
    @staticmethod
    def format_update_response(data: typing.Any = None, message: str = "Resource updated successfully") -> DataResponse:
        """格式化更新资源的成功响应"""
        return ResponseFormatter.format_response(data, 200, message)
    
    @staticmethod
    def format_delete_response(message: str = "Resource deleted successfully") -> DataResponse:
        """格式化删除资源的成功响应"""
        return ResponseFormatter.format_response({"deleted": True}, 200, message)
    
    @staticmethod
    def format_list_response(data: typing.Any = None, message: str = "Resources retrieved successfully") -> DataResponse:
        """格式化资源列表的成功响应"""
        return ResponseFormatter.format_response(data, 200, message)
    
    @staticmethod
    def format_retrieve_response(data: typing.Any = None, message: str = "Resource retrieved successfully") -> DataResponse:
        """格式化获取资源的成功响应"""
        return ResponseFormatter.format_response(data, 200, message)


# 创建单例
response_formatter = ResponseFormatter() 