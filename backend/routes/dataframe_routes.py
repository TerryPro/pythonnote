"""
DataFrame相关的API路由
"""
from typing import List, Dict, Any
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.data_explorer.data_loader import get_manager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()  # 移除prefix，因为已经在main.py中设置

class DataFrameInfoResponse(BaseModel):
    """DataFrame信息响应模型"""
    dataframes: List[str]
    status: str = "success"
    message: str = "Successfully retrieved DataFrame information"

class DataFramePreviewResponse(BaseModel):
    """DataFrame预览信息响应模型"""
    shape: tuple
    columns: Dict[str, str]
    memory_usage: int
    sample_data: Dict[str, List[Any]]
    status: str = "success"
    message: str = "Successfully retrieved DataFrame preview"

@router.get("/info", response_model=DataFrameInfoResponse)
async def get_dataframe_info() -> DataFrameInfoResponse:
    """
    获取所有已加载的DataFrame变量名
    
    Returns:
        DataFrameInfoResponse: 包含所有DataFrame变量名的响应对象
    """
    try:
        logger.info("正在获取DataFrame信息...")
        manager = get_manager()
        dataframes = manager.get_all_dataframes()
        logger.info(f"找到 {len(dataframes)} 个DataFrame")
        return DataFrameInfoResponse(dataframes=dataframes)
    except Exception as e:
        logger.error(f"获取DataFrame信息失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preview/{name}", response_model=DataFramePreviewResponse)
async def get_dataframe_preview(name: str) -> DataFramePreviewResponse:
    """
    获取指定DataFrame的预览信息
    
    Args:
        name: DataFrame变量名
        
    Returns:
        DataFramePreviewResponse: DataFrame的预览信息
    """
    try:
        logger.info(f"正在获取DataFrame {name} 的预览信息...")
        manager = get_manager()
        df = manager.get_dataframe(name)
        
        if df is None:
            raise HTTPException(status_code=404, detail=f"DataFrame {name} 不存在")
        
        preview_info = {
            "shape": df.shape,
            "columns": {col: str(df[col].dtype) for col in df.columns},
            "memory_usage": df.memory_usage(deep=True).sum(),
            "sample_data": df.head(5).to_dict(orient='list')
        }
        
        logger.info(f"成功获取DataFrame {name} 的预览信息")
        return DataFramePreviewResponse(**preview_info)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取DataFrame {name} 预览信息失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 