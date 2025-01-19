"""
AI相关的路由处理
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import numpy as np
import math
import json
from services.ai.deepseek_client import get_client

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NumpyJSONEncoder(json.JSONEncoder):
    """处理 NumPy 和特殊浮点数值的 JSON 编码器"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def handle_special_floats(obj):
    """处理特殊浮点数值的JSON序列化"""
    if isinstance(obj, (float, np.floating)):
        if math.isnan(obj) or np.isnan(obj):
            return None
        if math.isinf(obj) or np.isinf(obj):
            return None
    if isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: handle_special_floats(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [handle_special_floats(v) for v in obj]
    return obj

class GenerateCodeRequest(BaseModel):
    """代码生成请求模型"""
    prompt: str
    notebook_context: Optional[Dict[str, Any]] = None
    dataframe_info: Optional[Dict[str, Any]] = None
    dataframe_name: Optional[str] = None

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/generate_code")
async def generate_code(request: GenerateCodeRequest):
    """
    生成Python代码
    
    Args:
        request: 包含提示词和上下文信息的请求对象
        
    Returns:
        JSONResponse: 包含生成的代码的响应对象
    """
    try:
        logger.info("收到代码生成请求")
        logger.info(f"提示词: {request.prompt}")
        if request.dataframe_name:
            logger.info(f"DataFrame: {request.dataframe_name}")
        
        # 处理请求中的特殊浮点数值
        if request.dataframe_info:
            request.dataframe_info = handle_special_floats(request.dataframe_info)
        
        client = get_client()
        generated_code = await client.generate_code(
            prompt=request.prompt,
            dataframe_info=request.dataframe_info,
            dataframe_name=request.dataframe_name,
            notebook_context=request.notebook_context
        )
        
        # 使用自定义 JSON 编码器处理响应
        response_data = {
            "status": "success",
            "code": generated_code,
            "message": None
        }
        
        return JSONResponse(
            content=handle_special_floats(response_data),
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"代码生成失败: {str(e)}", exc_info=True)
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        ) 