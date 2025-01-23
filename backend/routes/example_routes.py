# 创建新文件
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from models.example import (
    Category, Example,
    CategoryCreate, CategoryUpdate,
    ExampleCreate, ExampleUpdate
)
from services.example_service import ExampleService

router = APIRouter(prefix="/api/code-examples", tags=["code-examples"])
example_service = ExampleService()

@router.get("/categories", response_model=List[Category])
async def get_categories():
    """获取所有分类"""
    return await example_service.get_categories()

@router.post("/categories", response_model=Category)
async def create_category(category: CategoryCreate):
    """创建分类"""
    return await example_service.create_category(category)

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(category_id: str, category: CategoryUpdate):
    """更新分类"""
    return await example_service.update_category(category_id, category)

@router.delete("/categories/{category_id}")
async def delete_category(category_id: str):
    """删除分类"""
    return await example_service.delete_category(category_id)

@router.get("/", response_model=List[Example])
async def get_examples():
    """获取所有示例"""
    return await example_service.get_examples()

@router.get("/category/{category_id}", response_model=List[Example])
async def get_category_examples(category_id: str):
    """获取分类下的所有示例"""
    return await example_service.get_category_examples(category_id)

@router.get("/{example_id}", response_model=Example)
async def get_example(example_id: str):
    """获取示例详情"""
    return await example_service.get_example(example_id)

@router.post("/", response_model=Example)
async def create_example(example: ExampleCreate):
    """创建示例"""
    return await example_service.create_example(example)

@router.put("/{example_id}", response_model=Example)
async def update_example(example_id: str, example: ExampleUpdate):
    """更新示例"""
    return await example_service.update_example(example_id, example)

@router.delete("/{example_id}")
async def delete_example(example_id: str):
    """删除示例"""
    return await example_service.delete_example(example_id)

@router.post("/{example_id}/use")
async def use_example(example_id: str):
    """使用示例"""
    return await example_service.use_example(example_id) 