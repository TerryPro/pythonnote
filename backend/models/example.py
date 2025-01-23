from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class Category(BaseModel):
    """代码分类模型"""
    id: str
    name: str
    description: str
    icon: str = "Document"

class Example(BaseModel):
    """代码示例模型"""
    id: str
    title: str
    description: str
    code: str
    category_id: str
    tags: List[str]
    use_count: int = 0
    created_at: datetime
    updated_at: datetime

class CategoryCreate(BaseModel):
    """创建分类请求模型"""
    name: str
    description: str
    icon: Optional[str] = None

class CategoryUpdate(BaseModel):
    """更新分类请求模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None

class ExampleCreate(BaseModel):
    """创建示例请求模型"""
    title: str
    description: str
    code: str
    category_id: str
    tags: List[str]

class ExampleUpdate(BaseModel):
    """更新示例请求模型"""
    title: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[List[str]] = None

class SaveFromCellRequest(BaseModel):
    """从单元格保存代码的请求模型"""
    code: str
    title: str
    description: str = ""
    category_id: str
    tags: List[str] = [] 