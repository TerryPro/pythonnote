"""
DataFrame相关的API路由
"""
from typing import List, Dict, Any
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import math
from app.services.data_explorer.data_loader import get_manager
from app.core.config import settings

# 配置日志
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dataframes", tags=["dataframes"])

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

class SaveDataFrameRequest(BaseModel):
    """保存DataFrame的请求模型"""
    file_path: str
    file_type: str = "csv"
    save_options: Dict[str, Any] = {}

def process_value(value: Any) -> Any:
    """处理数值，确保JSON序列化安全
    
    Args:
        value: 需要处理的值
        
    Returns:
        处理后的值
    """
    try:
        # 处理 None
        if value is None:
            return None
            
        # 处理 Pandas Timestamp 和 datetime64
        if str(type(value)) in ["<class 'pandas._libs.tslibs.timestamps.Timestamp'>", 
                               "<class 'numpy.datetime64'>",
                               "<class 'pandas.Timestamp'>"]:
            logger.debug(f"将 Timestamp 值 {value} 转换为 ISO 格式字符串")
            return value.isoformat()
            
        # 处理 NumPy 数值类型
        if isinstance(value, (np.integer, np.floating)):
            # 处理 NaN 和 Inf
            if np.isnan(value) or math.isnan(float(value)):
                logger.debug(f"将 NaN 值转换为 None")
                return None
            if np.isinf(value) or math.isinf(float(value)):
                logger.debug(f"将 Inf 值转换为 None")
                return None
            # 转换为 Python 原生类型
            return float(value)
            
        # 处理 NumPy 数组
        if isinstance(value, np.ndarray):
            logger.debug(f"将 NumPy 数组转换为列表")
            return [process_value(x) for x in value.tolist()]
            
        # 处理其他类型
        return value
    except Exception as e:
        logger.error(f"处理值 {value} (类型: {type(value)}) 时出错: {str(e)}")
        return None

def process_dict(data: Dict) -> Dict:
    """递归处理字典中的所有值
    
    Args:
        data: 需要处理的字典
        
    Returns:
        处理后的字典
    """
    return {k: process_value(v) if not isinstance(v, dict) else process_dict(v) 
            for k, v in data.items()}

@router.get("/list")
async def get_dataframes() -> List[str]:
    """获取所有可用的DataFrame变量名列表"""
    manager = get_manager()
    return manager.get_all_dataframes()

@router.get("/info/{name}")
async def get_dataframe_info(name: str) -> Dict[str, Any]:
    """获取指定DataFrame的详细信息
    
    Args:
        name: DataFrame变量名
        
    Returns:
        Dict包含DataFrame的详细信息
    """
    try:
        logger.info(f"获取DataFrame '{name}' 的信息")
        manager = get_manager()
        df = manager.get_dataframe(name)
        
        if df is None:
            logger.warning(f"DataFrame '{name}' 未找到")
            raise HTTPException(status_code=404, detail=f"DataFrame '{name}' not found")
            
        # 获取基本信息
        basic_info = {
            "行数": len(df),
            "列数": len(df.columns),
            "内存占用": f"{df.memory_usage().sum() / 1024**2:.2f} MB"
        }
        logger.debug(f"基本信息: {basic_info}")
        
        # 获取列信息
        columns = []
        for col in df.columns:
            try:
                col_info = {
                    "name": str(col),
                    "type": str(df[col].dtype),
                    "null_count": int(df[col].isnull().sum())
                }
                columns.append(col_info)
            except Exception as e:
                logger.error(f"处理列 '{col}' 信息时出错: {str(e)}")
                continue
        logger.debug(f"列信息: {columns}")
        
        # 获取预览信息
        try:
            head_data = df.head().to_dict('records')
            head_data = [process_dict(row) for row in head_data]
            
            # 获取统计信息并处理特殊值
            describe_df = df.describe()
            # 将所有的 nan 值替换为 None
            describe_df = describe_df.where(describe_df.notna(), None)
            summary_data = describe_df.to_dict()
            summary_data = process_dict(summary_data)
            
            preview = {
                "head": head_data,
                "summary": summary_data
            }
            logger.debug("预览信息已处理")
            logger.debug(f"处理后的预览信息: {preview}")
        except Exception as e:
            logger.error(f"处理预览信息时出错: {str(e)}")
            preview = {
                "head": [],
                "summary": {}
            }
        
        result = {
            "basic_info": basic_info,
            "columns": columns,
            "preview": preview
        }
        
        logger.info(f"成功获取DataFrame '{name}' 的信息")
        logger.info(result)
        return result
        
    except Exception as e:
        logger.error(f"获取DataFrame '{name}' 信息时发生错误: {str(e)}", exc_info=True)
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

@router.post("/{name}/save", response_model=Dict[str, Any])
async def save_dataframe(name: str, request: SaveDataFrameRequest) -> Dict[str, Any]:
    """
    保存指定的DataFrame到文件
    
    Args:
        name: DataFrame变量名
        request: SaveDataFrameRequest对象,包含保存选项
        
    Returns:
        Dict包含保存结果信息
    """
    try:
        logger.info(f"正在保存DataFrame {name} 到文件 {request.file_path}...")
        manager = get_manager()
        
        result = manager.save_dataframe(
            name=name,
            file_path=request.file_path,
            file_type=request.file_type,
            **request.save_options
        )
        
        logger.info(f"DataFrame {name} 保存成功")
        return result
        
    except ValueError as e:
        logger.error(f"保存DataFrame {name} 失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"保存DataFrame {name} 时发生错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 