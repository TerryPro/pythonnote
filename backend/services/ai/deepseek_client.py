"""
DeepSeek API Client for code generation.
"""
import os
import logging
from typing import Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

class DeepSeekClient:
    """DeepSeek API 客户端类"""
    
    def __init__(self):
        """初始化 DeepSeek 客户端"""
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        
        self.api_base = os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
        logger.info(f"初始化 DeepSeek 客户端 - API Base: {self.api_base}")
        
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base
            )
            logger.info("OpenAI 客户端初始化成功")
        except Exception as e:
            logger.error(f"OpenAI 客户端初始化失败: {str(e)}")
            raise

    async def generate_code(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        生成代码的异步方法
        
        Args:
            prompt: 用户的提示词
            context: 可选的上下文信息
            
        Returns:
            str: 生成的代码
            
        Raises:
            Exception: API调用失败时抛出异常
        """
        try:
            # 构建系统提示词
            system_content = "你是一个Python专家，按照用户的要求生成Python代码。"
            if context:
                system_content += f"\nContext: {context}"
            
            # 构建请求
            logger.info("准备发送请求到 DeepSeek API")
            logger.info(f"提示词: {prompt}")
            logger.info(f"系统提示词: {system_content}")
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                stream=False
            )
            logger.info("收到 DeepSeek API 响应")
            
            # 提取生成的代码
            generated_code = response.choices[0].message.content
            logger.info(f"生成的代码长度: {len(generated_code)}")
            
            return generated_code
            
        except Exception as e:
            logger.error(f"代码生成失败: {str(e)}", exc_info=True)
            raise Exception(f"Failed to generate code: {str(e)}")
        
    async def close(self):
        """关闭客户端（保持方法签名一致）"""
        pass

# 创建单例实例
_client: Optional[DeepSeekClient] = None

def get_client() -> DeepSeekClient:
    """获取DeepSeekClient的单例实例"""
    global _client
    if _client is None:
        _client = DeepSeekClient()
    return _client 