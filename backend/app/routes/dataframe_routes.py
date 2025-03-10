"""
DataFrame相关的API路由
"""
from typing import List, Dict, Any
import logging
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import numpy as np
import math
from app.core.config import settings
from app.services.code_executor.note_executor import get_executor

# 配置日志
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dataframes", tags=["dataframes"])

class DataFrameInfoResponse(BaseModel):
    """DataFrame信息响应模型"""
    status: str
    data: Dict[str, Any]
    message: str

class DataFrameInfoData(BaseModel):
    basic_info: Dict[str, Any]
    columns: Dict[str, str]
    memory_usage: int
    sample_data: Dict[str, List[Any]]
class DataFramePreviewResponse(BaseModel):
    """DataFrame预览信息响应模型"""
    status: str = "success"
    data: DataFrameInfoData
    message: str = "Successfully retrieved DataFrame preview"

class SaveDataFrameRequest(BaseModel):
    """保存DataFrame的请求模型"""
    session_id: str
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
async def get_dataframes(session_id: str) -> dict:
    executor = get_executor()
    dataframes = executor.get_dataframes_names(session_id)
    return {"status": "success", "data": dataframes}

@router.get("/info", response_model=DataFrameInfoResponse)
async def get_dataframe_info(session_id: str, name: str) -> DataFrameInfoResponse:
    """获取指定DataFrame的详细信息
    
    Args:
        name: DataFrame变量名
        
    Returns:
        DataFrameInfoResponse: 包含状态、数据和消息的字典
    """
    try:
        logger.info(f"获取DataFrame '{name}' 的信息")
        
        executor = get_executor()
        df = executor.get_dataframe(session_id, name)
        
        if df is None:
            logger.warning(f"DataFrame '{name}' 未找到")
            return {"status": "error", "data": {}, "message": f"DataFrame '{name}' 不存在"}
        
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
        return {"status": "success", "data": result, "message": "获取信息成功"}
        
    except Exception as e:
        logger.error(f"获取DataFrame '{name}' 信息时发生错误: {str(e)}", exc_info=True)
        return {"status": "error", "data": {}, "message": str(e)}

@router.get("/preview/{name}", response_model=Dict[str, Any])
async def get_dataframe_preview(name: str, request: Request) -> Dict[str, Any]:
    """
    获取指定DataFrame的预览信息
    
    Args:
        name: DataFrame变量名
        
    Returns:
        Dict[str, Any]: 包含状态、数据和消息的字典
    """
    try:
        logger.info(f"正在获取DataFrame {name} 的预览信息...")
        
        data = await request.json()
        session_id = data.get("session_id", "")
        
        executor = get_executor()
        df = executor.get_dataframe(session_id, name)
        
        if df is None:
            return {"status": "error", "data": {}, "message": f"DataFrame {name} 不存在"}
        
        preview_info = {
            "shape": df.shape,
            "columns": {col: str(df[col].dtype) for col in df.columns},
            "memory_usage": df.memory_usage(deep=True).sum(),
            "sample_data": df.head(5).to_dict(orient='list')
        }
        
        logger.info(f"成功获取DataFrame {name} 的预览信息")
        return {"status": "success", "data": preview_info, "message": "获取预览信息成功"}
        
    except Exception as e:
        logger.error(f"获取DataFrame {name} 预览信息失败: {str(e)}", exc_info=True)
        return {"status": "error", "data": {}, "message": str(e)}

@router.post("/save/{name}", response_model=Dict[str, Any])
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
        data = await request.json()
        session_id = data.get("session_id", "")
        executor = get_executor()       
        result = executor.save_dataframe_to_file(
            session_id=session_id,
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