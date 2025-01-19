from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_deepseek_api():
    print("=== 测试 DeepSeek API ===")
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    api_base = os.getenv('DEEPSEEK_API_BASE')
    
    print(f"API Base: {api_base}")
    print(f"API Key: {api_key[:8]}...")
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        
        print("\n发送测试请求...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a Python expert."},
                {"role": "user", "content": "Write a simple hello world program in Python."}
            ],
            stream=False
        )
        
        print("\n=== 响应内容 ===")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"\n错误: {str(e)}")
        print(f"错误类型: {type(e)}")

if __name__ == "__main__":
    test_deepseek_api() 