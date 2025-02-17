"""
DeepSeek代码生成客户端,支持直接访问和通过硅基流动访问
"""
import os
import json
import logging
import httpx
import requests
from typing import Dict, Any, Optional, Literal
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from abc import ABC, abstractmethod
from app.core.config import settings

# 配置日志
logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)
logger = logging.getLogger(__name__)

# 配置专门的提示词日志记录器
prompt_logger = logging.getLogger('prompt_logger')
prompt_logger.setLevel(logging.INFO)

# 创建日志处理器
prompt_handler = logging.FileHandler(
    settings.LOGS_DIR / 'prompts.log',
    encoding='utf-8'
)
prompt_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(message)s')
)
prompt_logger.addHandler(prompt_handler)

# 加载环境变量
load_dotenv()

class BaseDeepSeekClient(ABC):
    """DeepSeek基础客户端抽象类"""
    
    @abstractmethod
    def generate_code(
        self,
        prompt: str,
        dataframe_info: Optional[Dict[str, Any]] = None,
        dataframe_name: Optional[str] = None,
        notebook_context: Optional[Dict] = None
    ) -> str:
        """生成代码的抽象方法"""
        pass

class DirectDeepSeekClient(BaseDeepSeekClient):
    """直接访问DeepSeek的客户端类"""
    
    def __init__(self):
        """初始化客户端"""
        self.api_key = settings.DEEPSEEK_API_KEY
        if not self.api_key:
            raise ValueError("请在配置中设置DEEPSEEK_API_KEY")
            
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=settings.DEEPSEEK_API_BASE
        )
    
    def generate_code(
        self,
        prompt: str,
        dataframe_info: Optional[Dict[str, Any]] = None,
        dataframe_name: Optional[str] = None,
        notebook_context: Optional[Dict] = None
    ) -> str:
        """生成代码"""
        from .prompt_builder import PromptBuilder
        
        try:
            # 构建系统提示词
            system_prompt = PromptBuilder.build_system_prompt(dataframe_info)
            
            # 构建用户提示词
            user_prompt = PromptBuilder.build_user_prompt(prompt, dataframe_name) if dataframe_name else prompt
            
            # 记录最终的提示词到日志
            prompt_logger.info("系统提示词:")
            for line in system_prompt.split('\n'):
                if line.strip():  # 只记录非空行
                    prompt_logger.info(line)
            
            prompt_logger.info("\n用户提示词:")
            for line in user_prompt.split('\n'):
                if line.strip():  # 只记录非空行
                    prompt_logger.info(line)
            
            # 调用API生成代码
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=2000,
                stream=False
            )
            
            # 提取生成的代码
            generated_code = response.choices[0].message.content.strip()
            return generated_code
            
        except Exception as e:
            logger.error(f"代码生成失败: {str(e)}")
            raise

class SiliconFlowDeepSeekClient(BaseDeepSeekClient):
    """通过硅基流动访问DeepSeek的客户端类"""
    
    def __init__(self):
        """初始化客户端"""
        self.api_key = settings.SILICONFLOW_API_KEY
        if not self.api_key:
            raise ValueError("请在配置中设置SILICONFLOW_API_KEY")
            
        self.base_url = settings.SILICONFLOW_API_BASE
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_code(
        self,
        prompt: str,
        dataframe_info: Optional[Dict[str, Any]] = None,
        dataframe_name: Optional[str] = None,
        notebook_context: Optional[Dict] = None
    ) -> str:
        """生成代码"""
        from .prompt_builder import PromptBuilder
        
        try:
            # 构建系统提示词
            system_prompt = PromptBuilder.build_system_prompt(dataframe_info)
            
            # 构建用户提示词
            user_prompt = PromptBuilder.build_user_prompt(prompt, dataframe_name) if dataframe_name else prompt
            
            # 记录最终的提示词到日志
            prompt_logger.info("系统提示词:")
            for line in system_prompt.split('\n'):
                if line.strip():  # 只记录非空行
                    prompt_logger.info(line)
            
            prompt_logger.info("\n用户提示词:")
            for line in user_prompt.split('\n'):
                if line.strip():  # 只记录非空行
                    prompt_logger.info(line)
            
            # 准备请求数据
            payload = {
                "model": settings.DEEPSEEK_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "max_tokens": 2000,
                "temperature": 0.2,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {"type": "text"}
            }
            
            # 发送请求
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=self.headers
            )
            
            if response.status_code != 200:
                raise Exception(f"API请求失败: {response.text}")
            
            # 解析响应
            result = response.json()
            generated_code = result['choices'][0]['message']['content'].strip()
            return generated_code
            
        except Exception as e:
            logger.error(f"代码生成失败: {str(e)}")
            raise

class DeepSeekClientFactory:
    """DeepSeek客户端工厂类"""
    
    @staticmethod
    def create_client(client_type: Literal["direct", "siliconflow"] = "direct") -> BaseDeepSeekClient:
        """
        创建DeepSeek客户端
        
        Args:
            client_type: 客户端类型,"direct"表示直接访问,"siliconflow"表示通过硅基流动访问
            
        Returns:
            BaseDeepSeekClient: 客户端实例
        """
        logger.info(f"创建DeepSeek客户端: {client_type}")
        if client_type == "direct":
            return DirectDeepSeekClient()
        elif client_type == "siliconflow":
            return SiliconFlowDeepSeekClient()
        else:
            raise ValueError(f"不支持的客户端类型: {client_type}")

_client = None
_client_type = settings.DEEPSEEK_CLIENT_TYPE

def get_client() -> BaseDeepSeekClient:
    """
    获取DeepSeek客户端实例
    
    Returns:
        BaseDeepSeekClient: 客户端实例
    """
    global _client
    if _client is None:
        _client = DeepSeekClientFactory.create_client(_client_type)
    return _client 