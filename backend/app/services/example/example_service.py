# 创建新文件
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from fastapi import HTTPException
import logging
from app.models.example import (
    Category, Example,
    CategoryCreate, CategoryUpdate,
    ExampleCreate, ExampleUpdate
)
from app.core.config import settings

# 配置日志
logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)
logger = logging.getLogger(__name__)

class DateTimeEncoder(json.JSONEncoder):
    """处理datetime的JSON编码器"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class ExampleService:
    def __init__(self):
        self.data_dir = settings.EXAMPLES_DIR
        self.categories_file = self.data_dir / "categories.json"
        self.examples_dir = self.data_dir / "examples"
        
        # 确保目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.examples_dir.mkdir(parents=True, exist_ok=True)
        
        # 如果分类文件不存在，创建默认分类
        if not self.categories_file.exists():
            self._create_default_categories()

    def _create_default_categories(self):
        """创建默认分类"""
        default_categories = [
            {
                "id": "basic",
                "name": "基础语法",
                "description": "Python基础语法示例",
                "icon": "Document"
            },
            {
                "id": "data_types",
                "name": "数据类型",
                "description": "Python数据类型使用示例",
                "icon": "List"
            },
            {
                "id": "file_io",
                "name": "文件操作",
                "description": "文件读写操作示例",
                "icon": "Folder"
            },
            {
                "id": "data_process",
                "name": "数据处理",
                "description": "数据处理相关示例",
                "icon": "DataLine"
            },
            {
                "id": "algorithm",
                "name": "算法实现",
                "description": "常用算法示例",
                "icon": "CPU"
            }
        ]
        
        with open(self.categories_file, "w", encoding="utf-8") as f:
            json.dump({"categories": default_categories}, f, ensure_ascii=False, indent=2)
        
        # 为每个分类创建目录
        for category in default_categories:
            (self.examples_dir / category["id"]).mkdir(exist_ok=True)

    async def get_categories(self) -> List[Category]:
        """获取所有分类"""
        try:
            with open(self.categories_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Category(**category) for category in data["categories"]]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取分类失败: {str(e)}")

    async def create_category(self, category: CategoryCreate) -> Category:
        """创建分类"""
        try:
            # 读取现有分类
            with open(self.categories_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 生成新分类
            new_category = Category(
                id=str(uuid.uuid4()),
                name=category.name,
                description=category.description,
                icon=category.icon or "Document"
            )
            
            # 添加到列表
            data["categories"].append(new_category.dict())
            
            # 保存到文件
            with open(self.categories_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 创建分类目录
            (self.examples_dir / new_category.id).mkdir(exist_ok=True)
            
            return new_category
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"创建分类失败: {str(e)}")

    async def update_category(self, category_id: str, category: CategoryUpdate) -> Category:
        """更新分类"""
        try:
            # 读取现有分类
            with open(self.categories_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 查找并更新分类
            for i, cat in enumerate(data["categories"]):
                if cat["id"] == category_id:
                    # 更新非空字段
                    if category.name is not None:
                        cat["name"] = category.name
                    if category.description is not None:
                        cat["description"] = category.description
                    if category.icon is not None:
                        cat["icon"] = category.icon
                    
                    # 保存到文件
                    with open(self.categories_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    return Category(**cat)
            
            raise HTTPException(status_code=404, detail="分类不存在")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"更新分类失败: {str(e)}")

    async def delete_category(self, category_id: str):
        """删除分类"""
        try:
            # 读取现有分类
            with open(self.categories_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 查找并删除分类
            data["categories"] = [cat for cat in data["categories"] if cat["id"] != category_id]
            
            # 保存到文件
            with open(self.categories_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 删除分类目录及其内容
            category_dir = self.examples_dir / category_id
            if category_dir.exists():
                for file in category_dir.glob("*.json"):
                    file.unlink()
                category_dir.rmdir()
            
            return {"message": "删除成功"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"删除分类失败: {str(e)}")

    async def get_examples(self) -> List[Example]:
        """获取所有示例"""
        try:
            examples = []
            for category_dir in self.examples_dir.iterdir():
                if category_dir.is_dir():
                    for example_file in category_dir.glob("*.json"):
                        with open(example_file, "r", encoding="utf-8") as f:
                            example = json.load(f)
                            examples.append(Example(**example))
            return examples
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取示例失败: {str(e)}")

    async def get_category_examples(self, category_id: str) -> List[Example]:
        """获取分类下的所有示例"""
        try:
            examples = []
            category_dir = self.examples_dir / category_id
            if category_dir.exists():
                for example_file in category_dir.glob("*.json"):
                    with open(example_file, "r", encoding="utf-8") as f:
                        example = json.load(f)
                        examples.append(Example(**example))
            return examples
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取分类示例失败: {str(e)}")

    async def get_example(self, example_id: str) -> Example:
        """获取示例详情"""
        try:
            # 遍历所有分类目录查找示例
            for category_dir in self.examples_dir.iterdir():
                if category_dir.is_dir():
                    example_file = category_dir / f"{example_id}.json"
                    if example_file.exists():
                        with open(example_file, "r", encoding="utf-8") as f:
                            example = json.load(f)
                            return Example(**example)
            
            raise HTTPException(status_code=404, detail="示例不存在")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取示例失败: {str(e)}")

    async def create_example(self, example: ExampleCreate) -> Example:
        """创建示例"""
        try:
            logger.info(f"开始创建新示例，分类ID: {example.category_id}")
            
            # 检查分类是否存在
            category_dir = self.examples_dir / example.category_id
            if not category_dir.exists():
                logger.error(f"分类不存在: {example.category_id}")
                raise HTTPException(status_code=404, detail="分类不存在")
            
            # 生成新示例
            now = datetime.now()
            new_id = str(uuid.uuid4())
            logger.info(f"生成新示例ID: {new_id}")
            
            new_example = Example(
                id=new_id,
                title=example.title,
                description=example.description,
                code=example.code,
                category_id=example.category_id,
                tags=example.tags,
                use_count=0,
                created_at=now,
                updated_at=now
            )
            
            # 保存到文件
            example_file = category_dir / f"{new_example.id}.json"
            logger.info(f"保存示例到文件: {example_file}")
            
            try:
                with open(example_file, "w", encoding="utf-8") as f:
                    json.dump(new_example.dict(), f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
                logger.info("示例文件保存成功")
            except Exception as e:
                logger.error(f"保存示例文件失败: {str(e)}")
                raise Exception(f"保存示例文件失败: {str(e)}")
            
            return new_example
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"创建示例失败: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"创建示例失败: {str(e)}")

    async def update_example(self, example_id: str, example: ExampleUpdate) -> Example:
        """更新示例"""
        try:
            # 查找示例
            current_example = None
            example_file = None
            for category_dir in self.examples_dir.iterdir():
                if category_dir.is_dir():
                    file = category_dir / f"{example_id}.json"
                    if file.exists():
                        with open(file, "r", encoding="utf-8") as f:
                            current_example = Example(**json.load(f))
                            example_file = file
                            break
            
            if not current_example:
                raise HTTPException(status_code=404, detail="示例不存在")
            
            # 更新非空字段
            update_data = current_example.dict()
            if example.title is not None:
                update_data["title"] = example.title
            if example.description is not None:
                update_data["description"] = example.description
            if example.code is not None:
                update_data["code"] = example.code
            if example.category_id is not None:
                # 如果更改了分类，移动文件
                if example.category_id != current_example.category_id:
                    new_category_dir = self.examples_dir / example.category_id
                    if not new_category_dir.exists():
                        raise HTTPException(status_code=404, detail="目标分类不存在")
                    update_data["category_id"] = example.category_id
                    example_file.unlink()
                    example_file = new_category_dir / f"{example_id}.json"
            if example.tags is not None:
                update_data["tags"] = example.tags
            
            update_data["updated_at"] = datetime.now()
            
            # 保存更新
            updated_example = Example(**update_data)
            with open(example_file, "w", encoding="utf-8") as f:
                json.dump(updated_example.dict(), f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
            
            return updated_example
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"更新示例失败: {str(e)}")

    async def delete_example(self, example_id: str):
        """删除示例"""
        try:
            # 查找并删除示例文件
            for category_dir in self.examples_dir.iterdir():
                if category_dir.is_dir():
                    example_file = category_dir / f"{example_id}.json"
                    if example_file.exists():
                        example_file.unlink()
                        return {"message": "删除成功"}
            
            raise HTTPException(status_code=404, detail="示例不存在")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"删除示例失败: {str(e)}")

    async def use_example(self, example_id: str):
        """使用示例"""
        try:
            # 查找示例
            for category_dir in self.examples_dir.iterdir():
                if category_dir.is_dir():
                    example_file = category_dir / f"{example_id}.json"
                    if example_file.exists():
                        # 更新使用次数
                        with open(example_file, "r", encoding="utf-8") as f:
                            example = Example(**json.load(f))
                        
                        example.use_count += 1
                        example.updated_at = datetime.now()
                        
                        with open(example_file, "w", encoding="utf-8") as f:
                            json.dump(example.dict(), f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
                        
                        return {"message": "使用成功", "code": example.code}
            
            raise HTTPException(status_code=404, detail="示例不存在")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"使用示例失败: {str(e)}") 