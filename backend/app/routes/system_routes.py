''' 文件名称: system_routes.py
    功能: 定义系统相关的REST API接口，包括根路径欢迎信息和系统版本获取接口
    详细说明:
    - 使用FastAPI的APIRouter来配置API路由前缀和标签，便于分模块管理和文档生成。
    - 对每个接口增加了详细的注释，解释接口的功能、调用逻辑以及错误处理。
'''

from fastapi import APIRouter, HTTPException
import logging
from app.services.system.system_service import get_root_message, get_version_info

# 配置APIRouter，设置统一的路由前缀和标签，便于API文档归类和管理
router = APIRouter(prefix="/api/system", tags=["system"])

# 创建一个日志记录器，方便记录接口访问和错误日志
logger = logging.getLogger(__name__)

@router.get("/")
async def root():
    """
    根路径API，返回欢迎信息
    详细说明:
        - 当用户访问根路径时，会调用此接口返回一个欢迎信息。
        - 接口内部会记录访问日志，便于运维排查问题。
        - 调用get_root_message()方法获取欢迎信息，如遇异常则返回HTTP 500错误。
    """
    # 记录访问根路径的日志信息
    logger.info("访问根路径")
    try:
        # 调用系统服务获取根路径下的欢迎信息
        return get_root_message()
    except Exception as e:
        # 捕获所有异常，返回HTTP异常，带上错误详情便于调试
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/version")
async def get_version():
    """
    获取系统版本信息接口
    详细说明:
        - 此接口用于获取当前系统的版本信息。
        - 内部调用get_version_info()服务函数获取版本详情。
        - 如果返回的状态为错误，则抛出HTTP异常并返回错误信息。
    Returns:
        dict: 包含系统版本信息的字典，例如:
            {
                "version": "1.0.0",
                "status": "ok"
            }
    """
    # 调用系统服务函数获取系统版本信息
    info = get_version_info()
    # 判断返回信息中是否存在错误标识，若是则抛出HTTP异常
    if info.get("status") == "error":
        raise HTTPException(status_code=500, detail=info.get("detail", "未知错误"))
    # 返回包含系统版本信息的字典
    return info 