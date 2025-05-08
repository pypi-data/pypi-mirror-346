from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import traceback

from src.models.schemas.response import error_response, DataResponse
from src.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from src.utilities.exceptions.password import PasswordDoesNotMatch


# 将Pydantic模型转换为dict，兼容v1和v2
def model_to_dict(model):
    """将Pydantic模型转换为字典，兼容v1和v2"""
    if hasattr(model, "model_dump"):  # v2
        return model.model_dump()
    return model.dict()  # v1


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """处理参数验证错误"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=model_to_dict(error_response(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=f"Validation error: {str(exc)}"
        ))
    )


async def database_entity_not_found_handler(request: Request, exc: EntityDoesNotExist) -> JSONResponse:
    """处理数据库实体未找到错误"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=model_to_dict(error_response(
            code=status.HTTP_404_NOT_FOUND,
            message=str(exc)
        ))
    )


async def database_entity_already_exists_handler(request: Request, exc: EntityAlreadyExists) -> JSONResponse:
    """处理数据库实体已存在错误"""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=model_to_dict(error_response(
            code=status.HTTP_409_CONFLICT,
            message=str(exc)
        ))
    )


async def password_does_not_match_handler(request: Request, exc: PasswordDoesNotMatch) -> JSONResponse:
    """处理密码不匹配错误"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=model_to_dict(error_response(
            code=status.HTTP_401_UNAUTHORIZED,
            message=str(exc)
        ))
    )


async def pydantic_validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """处理Pydantic验证错误"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=model_to_dict(error_response(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=f"Data validation error: {str(exc)}"
        ))
    )


async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """处理通用内部错误"""
    # 开发环境显示详细错误
    error_detail = str(exc)
    trace = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=model_to_dict(error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Internal server error: {error_detail}"
        ))
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    注册所有异常处理器
    
    Args:
        app: FastAPI应用实例
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(EntityDoesNotExist, database_entity_not_found_handler)
    app.add_exception_handler(EntityAlreadyExists, database_entity_already_exists_handler)
    app.add_exception_handler(PasswordDoesNotMatch, password_does_not_match_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_error_handler)
    app.add_exception_handler(Exception, internal_exception_handler) 