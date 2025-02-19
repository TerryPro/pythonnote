"""
用户提示词配置管理模块
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any
from app.core.config import settings

class UserPromptConfig:
    """用户提示词配置管理类"""
    
    def __init__(self):
        # 配置文件路径
        self.config_path = os.path.join(settings.CONFIG_DIR, 'user_prompts.json')
        
        # 默认代码生成要求
        self.default_requirements = [
            "如果需要导入包，请在代码开头导入"
        ]
    
    def load_requirements(self) -> List[str]:
        """
        加载代码生成要求配置
        
        Returns:
            List[str]: 代码生成要求列表
        """
        try:
            if not os.path.exists(self.config_path):
                return self.default_requirements
                
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('code_requirements', self.default_requirements)
        except Exception as e:
            print(f"加载代码生成要求配置失败: {str(e)}")
            return self.default_requirements
    
    def save_requirements(self, requirements: List[str]) -> bool:
        """
        保存代码生成要求配置
        
        Args:
            requirements: 要保存的代码生成要求列表
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 确保配置目录存在
            os.makedirs(settings.CONFIG_DIR, exist_ok=True)
            
            config = {
                "version": "1.0",
                "last_modified": datetime.now().isoformat(),
                "code_requirements": requirements
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存代码生成要求配置失败: {str(e)}")
            return False
    
    def reset_requirements(self) -> bool:
        """
        重置为默认代码生成要求
        
        Returns:
            bool: 重置是否成功
        """
        return self.save_requirements(self.default_requirements) 