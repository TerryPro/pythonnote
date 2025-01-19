import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_generate_code():
    print("\n=== 开始API测试 ===")
    
    # 检查环境变量
    api_key = os.getenv('DEEPSEEK_API_KEY')
    api_base = os.getenv('DEEPSEEK_API_BASE')
    print(f"API Base URL: {api_base}")
    print(f"API Key 配置状态: {'已配置' if api_key else '未配置'}")
    
    url = "http://localhost:8000/api/ai/generate_code"
    data = {
        "prompt": "创建一个简单的数据框，包含姓名和年龄两列，并计算年龄的平均值",
        "notebook_context": {
            "imports": ["import pandas as pd", "import numpy as np"],
            "variables": {}
        },
        "dataframe_info": {}
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    print("\n--- 请求信息 ---")
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    try:
        async with aiohttp.ClientSession() as session:
            print("\n--- 发送请求 ---")
            async with session.post(url, json=data, headers=headers) as response:
                print(f"状态码: {response.status}")
                print(f"响应头: {dict(response.headers)}")
                
                response_text = await response.text()
                print(f"\n--- 原始响应 ---\n{response_text}")
                
                if response.status == 200:
                    try:
                        response_json = await response.json()
                        print("\n--- 生成的代码 ---")
                        print(response_json.get("code", "无代码返回"))
                    except json.JSONDecodeError as e:
                        print(f"JSON解析错误: {str(e)}")
                else:
                    print(f"请求失败: HTTP {response.status}")
                    
    except aiohttp.ClientConnectorError:
        print("连接错误：请确保后端服务已启动")
    except Exception as e:
        print(f"发生错误: {str(e)}")
        print(f"错误类型: {type(e)}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    asyncio.run(test_generate_code()) 