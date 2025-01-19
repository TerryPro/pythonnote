"""
AI service routes for code generation.
"""
from typing import Dict, Optional
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.ai.deepseek_client import get_client
from services.ai.prompt_builder import PromptBuilder

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["ai"])

class CodeGenerationRequest(BaseModel):
    """代码生成请求模型"""
    prompt: str
    notebook_context: Optional[Dict] = None
    dataframe_info: Optional[Dict] = None

class CodeGenerationResponse(BaseModel):
    """代码生成响应模型"""
    code: str
    status: str = "success"
    message: Optional[str] = None

@router.post("/generate_code", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest) -> CodeGenerationResponse:
    """
    生成代码的API端点
    
    Args:
        request: 包含提示词和上下文信息的请求对象
        
    Returns:
        包含生成的代码的响应对象
        
    Raises:
        HTTPException: 当代码生成失败时抛出异常
    """
    try:
        logger.info(f"收到代码生成请求: {request.prompt}")
        logger.info(f"笔记本上下文: {request.notebook_context}")
        logger.info(f"DataFrame信息: {request.dataframe_info}")
        
        # 获取AI客户端
        client = get_client()
        logger.info("成功获取AI客户端")
        
        # 构建提示词
        prompt = PromptBuilder.build_code_generation_prompt(
            user_request=request.prompt,
            notebook_context=request.notebook_context,
            dataframe_info=request.dataframe_info
        )
        logger.info(f"构建的提示词: {prompt}")
        
        # 生成代码
        logger.info("开始生成代码...")
        response = await client.generate_code(prompt)
        logger.info("代码生成完成")
        
        # 从响应中提取代码
        code = PromptBuilder.extract_code_from_response(response)
        logger.info(f"提取的代码: {code}")
        
        return CodeGenerationResponse(
            code=code,
            status="success"
        )
        
    except Exception as e:
        logger.error(f"代码生成失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"代码生成失败: {str(e)}"
        ) 