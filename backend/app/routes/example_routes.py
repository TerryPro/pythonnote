# 创建新文件
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
import logging
from app.models.example import (
    Category, Example,
    CategoryCreate, CategoryUpdate,
    ExampleCreate, ExampleUpdate,
    SaveFromCellRequest
)
from app.services.example import ExampleService

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@router.post("/save-from-cell", response_model=Example)
async def save_from_cell(request: SaveFromCellRequest):
    """从单元格保存代码到示例库"""
    try:
        logger.info("接收到保存示例请求:")
        logger.info(f"标题: {request.title}")
        logger.info(f"描述: {request.description}")
        logger.info(f"分类ID: {request.category_id}")
        logger.info(f"标签: {request.tags}")
        logger.info(f"代码长度: {len(request.code)} 字符")
        
        example = ExampleCreate(
            title=request.title,
            description=request.description,
            code=request.code,
            category_id=request.category_id,
            tags=request.tags
        )
        
        logger.info("开始创建示例...")
        result = await example_service.create_example(example)
        logger.info(f"示例创建成功，ID: {result.id}")
        return result
        
    except Exception as e:
        logger.error(f"创建示例失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"创建示例失败: {str(e)}") 