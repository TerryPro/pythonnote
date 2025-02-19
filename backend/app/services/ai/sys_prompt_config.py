"""
系统提示词配置管理模块
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any
from app.core.config import settings  # 导入新的配置目录

class SysPromptConfig:
    """系统提示词配置管理类"""
    
    def __init__(self):
        # 配置文件路径
        self.config_path = os.path.join(settings.CONFIG_DIR, 'system_prompts.json')  # 使用CONFIG_DIR
        
        # 默认提示词列表
        self.default_prompts = [
            "你是一个Python数据分析专家，精通pandas库的使用。",
            "你需要根据用户的需求，生成准确的Python代码。",
            "生成的代码应该：",
            "1. 代码简洁易懂，有必要的注释",
            "2. 使用pandas的最佳实践",
            "3. 考虑数据处理的性能",
            "4. 包含适当的错误处理",
            "5. 在检查变量是否存在时，使用 'df' in locals() 而不是 globals()",
            "6. DataFrame存在性检查使用 'df' in locals() and not df.empty",
            "7. 当生成多幅图时使用子图的方式",
            "8. 只返回可以直接执行的Python代码",
            "9. 不要使用任何Markdown格式", 
            "10. 不要使用```python或```等代码块标记",
            "11. 不要包含任何自然语言解释",
            "12. 代码中包含必要的注释（使用#号注释）"
        ]
    
    def load_prompts(self) -> List[str]:
        """
        加载提示词配置
        
        Returns:
            List[str]: 提示词列表
        """
        try:
            if not os.path.exists(self.config_path):
                return self.default_prompts
                
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('prompts', self.default_prompts)
        except Exception as e:
            print(f"加载提示词配置失败: {str(e)}")
            return self.default_prompts
    
    def save_prompts(self, prompts: List[str]) -> bool:
        """
        保存提示词配置
        
        Args:
            prompts: 要保存的提示词列表
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 确保配置目录存在
            os.makedirs(settings.CONFIG_DIR, exist_ok=True)
            
            config = {
                "version": "1.0",
                "last_modified": datetime.now().isoformat(),
                "prompts": prompts
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存提示词配置失败: {str(e)}")
            return False
    
    def reset_prompts(self) -> bool:
        """
        重置为默认提示词
        
        Returns:
            bool: 重置是否成功
        """
        return self.save_prompts(self.default_prompts) 