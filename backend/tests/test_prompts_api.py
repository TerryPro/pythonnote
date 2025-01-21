import requests
import pytest

BASE_URL = "http://localhost:8000/api/ai"

def test_get_system_prompts():
    """测试获取系统提示词"""
    response = requests.get(f"{BASE_URL}/system-prompts")
    assert response.status_code == 200
    prompts = response.json()
    assert isinstance(prompts, list)
    assert len(prompts) > 0
    print("当前提示词配置：")
    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. {prompt}")

def test_update_system_prompts():
    """测试更新系统提示词"""
    new_prompts = [
        "你是一个Python数据分析专家，精通pandas和matplotlib库的使用。",
        "你需要根据用户的需求，生成准确的Python代码。",
        "生成的代码应该：",
        "1. 代码简洁易懂，有必要的注释",
        "2. 使用pandas和matplotlib的最佳实践",
        "3. 考虑数据处理的性能",
        "4. 包含适当的错误处理"
    ]
    
    response = requests.put(
        f"{BASE_URL}/system-prompts",
        json={"prompts": new_prompts}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    print("\n提示词更新成功！")

def test_reset_system_prompts():
    """测试重置系统提示词"""
    response = requests.post(f"{BASE_URL}/system-prompts/reset")
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    print("\n提示词重置成功！")

if __name__ == "__main__":
    # 测试获取当前配置
    print("=== 测试获取当前配置 ===")
    test_get_system_prompts()
    
    # 测试更新配置
    print("\n=== 测试更新配置 ===")
    test_update_system_prompts()
    
    # 验证更新后的配置
    print("\n=== 验证更新后的配置 ===")
    test_get_system_prompts()
    
    # 测试重置配置
    print("\n=== 测试重置配置 ===")
    test_reset_system_prompts()
    
    # 验证重置后的配置
    print("\n=== 验证重置后的配置 ===")
    test_get_system_prompts() 