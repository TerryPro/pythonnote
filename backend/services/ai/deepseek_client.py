"""
DeepSeek代码生成客户端
"""
import os
import json
import logging
import httpx
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置专门的提示词日志记录器
prompt_logger = logging.getLogger('prompt_logger')
prompt_logger.setLevel(logging.INFO)

# 创建日志处理器
prompt_handler = logging.FileHandler(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                'logs', 'prompts.log'),
    encoding='utf-8'
)
prompt_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(message)s')
)
prompt_logger.addHandler(prompt_handler)

# 加载环境变量
load_dotenv()

class DeepSeekClient:
    """DeepSeek API客户端类"""
    
    def __init__(self):
        """初始化客户端"""
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("未找到DEEPSEEK_API_KEY环境变量")
            
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
    
    def generate_code(
        self,
        prompt: str,
        dataframe_info: Optional[Dict[str, Any]] = None,
        dataframe_name: Optional[str] = None,
        notebook_context: Optional[Dict] = None
    ) -> str:
        """
        生成代码
        
        Args:
            prompt: 用户提示词
            dataframe_info: DataFrame信息
            dataframe_name: DataFrame变量名
            notebook_context: 笔记本上下文
            
        Returns:
            str: 生成的代码
        """
        from .prompt_builder import PromptBuilder
        
        try:
            # 构建系统提示词
            system_prompt = PromptBuilder.build_system_prompt(dataframe_info)
            
            # 构建用户提示词
            user_prompt = PromptBuilder.build_user_prompt(prompt, dataframe_name) if dataframe_name else prompt
            
            # 记录最终的提示词到日志
            prompt_logger.info(
                "系统提示词:\n%s\n用户提示词:\n%s", 
                system_prompt, 
                user_prompt
            )
            
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

_client = None

def get_client() -> DeepSeekClient:
    """
    获取DeepSeek客户端实例
    
    Returns:
        DeepSeekClient: 客户端实例
    """
    global _client
    if _client is None:
        _client = DeepSeekClient()
    return _client 