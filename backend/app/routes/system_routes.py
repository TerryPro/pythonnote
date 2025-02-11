from fastapi import APIRouter, HTTPException
import logging
from app.core.config import settings
from app.core.version import VERSION

router = APIRouter(tags=["system"])

logger = logging.getLogger(__name__)

@router.get("/")
async def root():
    """
    根路径API，返回欢迎信息
    """
    logger.info("访问根路径")
    return {"message": "Welcome to AI Code Generator API"} 

@router.get("/api/version")
async def get_version():
    """
    获取系统版本信息
    
    Returns:
        dict: 包含系统版本信息的字典
    """
    try:
        return {
            "status": "success",
            "data": VERSION
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 