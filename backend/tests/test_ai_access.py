import os
import json
import logging
from typing import Dict, Any, Optional, Literal
from openai import OpenAI
import requests
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

class DeepSeekTester:
    """DeepSeek API测试类"""
    
    def __init__(self):
        """初始化测试器"""
        self.client_type = os.getenv('DEEPSEEK_CLIENT_TYPE', 'direct')
        self._init_client()
        
    def _init_client(self):
        """初始化客户端"""
        if self.client_type == "direct":
            self._init_direct_client()
        elif self.client_type == "siliconflow":
            self._init_siliconflow_client()
        else:
            raise ValueError(f"不支持的客户端类型: {self.client_type}")
            
    def _init_direct_client(self):
        """初始化直接访问客户端"""
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("未找到DEEPSEEK_API_KEY环境变量")
            
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        
    def _init_siliconflow_client(self):
        """初始化硅基流动客户端"""
        self.api_key = os.getenv('SILICONFLOW_API_KEY')
        if not self.api_key:
            raise ValueError("未找到SILICONFLOW_API_KEY环境变量")
            
        self.base_url = "https://api.siliconflow.cn/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def test_generate_code(self) -> None:
        """测试代码生成功能"""
        logger.info(f"\n=== 开始测试 DeepSeek API ({self.client_type}模式) ===")
        
        # 测试用例列表
        test_cases = [
            {
                "name": "Python基础代码",
                "system_prompt": "You are a Python expert.",
                "user_prompt": "Write a simple hello world program in Python."
            },
            {
                "name": "数据处理代码",
                "system_prompt": """You are a data analysis expert. 
                Current DataFrame 'df' has columns: ['name', 'age', 'salary'].""",
                "user_prompt": "Calculate average salary grouped by age ranges (20-30, 31-40, 41-50)."
            }
        ]
        
        for test_case in test_cases:
            try:
                logger.info(f"\n--- 执行测试用例: {test_case['name']} ---")
                response = self._generate_code(
                    test_case["system_prompt"],
                    test_case["user_prompt"]
                )
                logger.info("\n生成的代码:")
                logger.info(response)
            except Exception as e:
                logger.error(f"测试用例 {test_case['name']} 失败: {str(e)}")
                logger.error(f"错误类型: {type(e)}")
    
    def _generate_code(self, system_prompt: str, user_prompt: str) -> str:
        """生成代码
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            
        Returns:
            str: 生成的代码
        """
        try:
            if self.client_type == "direct":
                return self._generate_code_direct(system_prompt, user_prompt)
            else:
                return self._generate_code_siliconflow(system_prompt, user_prompt)
        except Exception as e:
            logger.error(f"代码生成失败: {str(e)}")
            raise
            
    def _generate_code_direct(self, system_prompt: str, user_prompt: str) -> str:
        """使用直接访问模式生成代码"""
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
        return response.choices[0].message.content.strip()
        
    def _generate_code_siliconflow(self, system_prompt: str, user_prompt: str) -> str:
        """使用硅基流动模式生成代码"""
        payload = {
            "model": "deepseek-ai/DeepSeek-V3",
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
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers=self.headers
        )
        
        if response.status_code != 200:
            raise Exception(f"API请求失败: {response.text}")
            
        result = response.json()
        return result['choices'][0]['message']['content'].strip()

def main():
    """主函数"""
    try:
        tester = DeepSeekTester()
        tester.test_generate_code()
    except Exception as e:
        logger.error(f"测试执行失败: {str(e)}")
        logger.error(f"错误类型: {type(e)}")

if __name__ == "__main__":
    main() 