"""
AI相关的路由处理
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
import numpy as np
import math
import json
from services.ai.deepseek_client import get_client
from services.ai.sys_prompt_config import SysPromptConfig
from services.ai.user_prompt_config import UserPromptConfig

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

# 添加新的请求模型
class UpdatePromptsRequest(BaseModel):
    """更新提示词请求模型"""
    prompts: List[str]

# 添加新的请求模型
class UpdateUserPromptsRequest(BaseModel):
    """更新用户提示词请求模型"""
    requirements: List[str]

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

# 添加新的路由处理
@router.get("/system-prompts", response_model=List[str])
async def get_system_prompts():
    """
    获取当前系统提示词
    
    Returns:
        List[str]: 提示词列表
    """
    try:
        config = SysPromptConfig()
        prompts = config.load_prompts()
        return prompts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/system-prompts")
async def update_system_prompts(request: UpdatePromptsRequest):
    """
    更新系统提示词
    
    Args:
        request: 包含新提示词列表的请求对象
    
    Returns:
        Dict: 更新结果
    """
    try:
        config = SysPromptConfig()
        success = config.save_prompts(request.prompts)
        if success:
            return {"status": "success", "message": "提示词更新成功"}
        else:
            raise HTTPException(status_code=500, detail="提示词更新失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/system-prompts/reset")
async def reset_system_prompts():
    """
    重置系统提示词为默认值
    
    Returns:
        Dict: 重置结果
    """
    try:
        config = SysPromptConfig()
        success = config.reset_prompts()
        if success:
            return {"status": "success", "message": "提示词已重置为默认值"}
        else:
            raise HTTPException(status_code=500, detail="提示词重置失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 添加用户提示词配置相关的路由
@router.get("/user-prompts", response_model=List[str])
async def get_user_prompts():
    """
    获取当前用户提示词配置
    
    Returns:
        List[str]: 代码生成要求列表
    """
    try:
        config = UserPromptConfig()
        requirements = config.load_requirements()
        return requirements
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/user-prompts")
async def update_user_prompts(request: UpdateUserPromptsRequest):
    """
    更新用户提示词配置
    
    Args:
        request: 包含新代码生成要求列表的请求对象
    
    Returns:
        Dict: 更新结果
    """
    try:
        config = UserPromptConfig()
        success = config.save_requirements(request.requirements)
        if success:
            return {"status": "success", "message": "代码生成要求更新成功"}
        else:
            raise HTTPException(status_code=500, detail="代码生成要求更新失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user-prompts/reset")
async def reset_user_prompts():
    """
    重置用户提示词配置为默认值
    
    Returns:
        Dict: 重置结果
    """
    try:
        config = UserPromptConfig()
        success = config.reset_requirements()
        if success:
            return {"status": "success", "message": "代码生成要求已重置为默认值"}
        else:
            raise HTTPException(status_code=500, detail="代码生成要求重置失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 