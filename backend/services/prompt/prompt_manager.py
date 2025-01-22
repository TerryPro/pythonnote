import json
from pathlib import Path
from typing import Dict, List, Optional
import uuid

class PromptManager:
    def __init__(self, config_path: str = "config/prompt_templates.json"):
        self.config_path = config_path
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """加载提示词模板配置"""
        config_file = Path(self.config_path)
        if not config_file.exists():
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_templates(self) -> bool:
        """保存提示词模板配置"""
        try:
            config_file = Path(self.config_path)
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存提示词模板失败: {str(e)}")
            return False

    def get_categories(self) -> List[Dict]:
        """获取所有提示词分类"""
        categories = []
        for category_id, category_data in self.templates.items():
            categories.append({
                "id": category_id,
                "name": category_data["category_name"],
                "description": category_data["category_description"]
            })
        return categories

    def get_category_prompts(self, category_id: str) -> List[Dict]:
        """获取指定分类下的所有提示词"""
        if category_id not in self.templates:
            return []
        return self.templates[category_id]["prompts"]

    def get_prompt(self, prompt_id: str) -> Optional[Dict]:
        """获取单个提示词详情"""
        for category in self.templates.values():
            for prompt in category["prompts"]:
                if prompt["id"] == prompt_id:
                    return prompt
        return None

    def increment_use_count(self, prompt_id: str) -> bool:
        """增加提示词使用次数"""
        for category in self.templates.values():
            for prompt in category["prompts"]:
                if prompt["id"] == prompt_id:
                    prompt["use_count"] += 1
                    return self._save_templates()
        return False

    def create_category(self, category_data: Dict) -> bool:
        """创建新分类"""
        category_id = str(uuid.uuid4())
        self.templates[category_id] = {
            "category_name": category_data["name"],
            "category_description": category_data["description"],
            "prompts": []
        }
        return self._save_templates()

    def update_category(self, category_id: str, category_data: Dict) -> bool:
        """更新分类"""
        if category_id not in self.templates:
            return False
        self.templates[category_id].update({
            "category_name": category_data["name"],
            "category_description": category_data["description"]
        })
        return self._save_templates()

    def create_prompt(self, prompt_data: Dict) -> bool:
        """创建新提示词"""
        category_id = prompt_data["category_id"]
        if category_id not in self.templates:
            return False
        
        prompt = {
            "id": str(uuid.uuid4()),
            "title": prompt_data["title"],
            "description": prompt_data["description"],
            "template": prompt_data["template"],
            "tags": prompt_data["tags"],
            "use_count": 0
        }
        self.templates[category_id]["prompts"].append(prompt)
        return self._save_templates()

    def update_prompt(self, prompt_id: str, prompt_data: Dict) -> bool:
        """更新提示词"""
        for category_id, category in self.templates.items():
            for i, prompt in enumerate(category["prompts"]):
                if prompt["id"] == prompt_id:
                    # 如果分类改变了
                    if prompt_data["category_id"] != category_id:
                        # 从原分类中删除
                        category["prompts"].pop(i)
                        # 添加到新分类
                        new_prompt = {
                            "id": prompt_id,
                            "title": prompt_data["title"],
                            "description": prompt_data["description"],
                            "template": prompt_data["template"],
                            "tags": prompt_data["tags"],
                            "use_count": prompt["use_count"]
                        }
                        self.templates[prompt_data["category_id"]]["prompts"].append(new_prompt)
                    else:
                        # 更新现有提示词
                        prompt.update({
                            "title": prompt_data["title"],
                            "description": prompt_data["description"],
                            "template": prompt_data["template"],
                            "tags": prompt_data["tags"]
                        })
                    return self._save_templates()
        return False

    def delete_prompt(self, prompt_id: str) -> bool:
        """删除提示词"""
        for category in self.templates.values():
            for i, prompt in enumerate(category["prompts"]):
                if prompt["id"] == prompt_id:
                    category["prompts"].pop(i)
                    return self._save_templates()
        return False 