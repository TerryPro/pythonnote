import asyncio
import aiohttp
import json
import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

class APITester:
    """API测试类"""
    
    def __init__(self):
        """初始化测试器"""
        self.base_url = "http://localhost:8000"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
    async def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送API请求
        
        Args:
            endpoint: API端点
            data: 请求数据
            
        Returns:
            Dict[str, Any]: API响应
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"\n--- 请求信息 ---\nURL: {url}\nHeaders: {json.dumps(self.headers, indent=2)}")
        logger.info(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        try:
            async with aiohttp.ClientSession() as session:
                logger.info("\n--- 发送请求 ---")
                async with session.post(url, json=data, headers=self.headers) as response:
                    logger.info(f"状态码: {response.status}")
                    logger.info(f"响应头: {dict(response.headers)}")
                    
                    response_text = await response.text()
                    logger.info(f"\n--- 原始响应 ---\n{response_text}")
                    
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise Exception(f"请求失败: HTTP {response.status}")
                        
        except aiohttp.ClientConnectorError:
            raise Exception("连接错误：请确保后端服务已启动")
        except Exception as e:
            logger.error(f"发生错误: {str(e)}")
            logger.error(f"错误类型: {type(e)}")
            raise

    async def test_generate_code(self) -> None:
        """测试代码生成API"""
        logger.info("\n=== 开始代码生成API测试 ===")
        
        # 检查环境变量
        self._check_environment()
        
        # 测试用例列表
        test_cases = [
            {
                "name": "基础数据框操作",
                "data": {
                    "prompt": "创建一个简单的数据框，包含姓名和年龄两列，并计算年龄的平均值",
                    "notebook_context": {
                        "imports": ["import pandas as pd", "import numpy as np"],
                        "variables": {}
                    },
                    "dataframe_info": {}
                }
            },
            {
                "name": "数据分析操作",
                "data": {
                    "prompt": "对sales数据进行分组统计，计算每个类别的销售总额和平均值",
                    "notebook_context": {
                        "imports": ["import pandas as pd"],
                        "variables": {"sales": "pd.DataFrame({'category': ['A', 'B', 'A', 'C'], 'amount': [100, 200, 150, 300]})"}
                    },
                    "dataframe_info": {
                        "sales": {
                            "columns": ["category", "amount"],
                            "dtypes": {"category": "object", "amount": "int64"}
                        }
                    }
                }
            }
        ]
        
        # 执行测试用例
        for test_case in test_cases:
            try:
                logger.info(f"\n--- 执行测试用例: {test_case['name']} ---")
                response = await self._make_request("/api/ai/generate_code", test_case["data"])
                logger.info("\n--- 生成的代码 ---")
                logger.info(response.get("code", "无代码返回"))
            except Exception as e:
                logger.error(f"测试用例 {test_case['name']} 失败: {str(e)}")
    
    def _check_environment(self) -> None:
        """检查环境变量配置"""
        required_vars = {
            'DEEPSEEK_API_KEY': '直接访问模式的API密钥',
            'DEEPSEEK_API_BASE': 'DeepSeek API基础URL',
            'SILICONFLOW_API_KEY': '硅基流动模式的API密钥',
            'DEEPSEEK_CLIENT_TYPE': '客户端类型(direct/siliconflow)'
        }
        
        logger.info("\n--- 环境变量检查 ---")
        for var, description in required_vars.items():
            value = os.getenv(var)
            status = '已配置' if value else '未配置'
            logger.info(f"{description} ({var}): {status}")

async def main():
    """主函数"""
    tester = APITester()
    await tester.test_generate_code()

if __name__ == "__main__":
    asyncio.run(main()) 