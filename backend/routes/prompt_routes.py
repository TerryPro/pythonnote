"""
提示词相关的API路由
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Generic, TypeVar
from services.prompt.prompt_manager import PromptManager

router = APIRouter(prefix="/api/prompt", tags=["prompts"])
prompt_manager = PromptManager()

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    """统一响应模型"""
    code: int = 200
    data: T
    message: str = "success"

class CategoryResponse(BaseModel):
    """分类响应模型"""
    id: str
    name: str
    description: str

class PromptResponse(BaseModel):
    """提示词响应模型"""
    id: str
    title: str
    description: str
    template: str
    tags: List[str]
    use_count: int

class CategoryRequest(BaseModel):
    """分类请求模型"""
    name: str
    description: str

class PromptRequest(BaseModel):
    """提示词请求模型"""
    title: str
    description: str
    template: str
    tags: List[str]
    category_id: str

@router.get("/categories", response_model=ResponseModel[List[CategoryResponse]])
async def get_categories():
    """获取所有提示词分类"""
    categories = prompt_manager.get_categories()
    return ResponseModel(data=categories)

@router.get("/category/{category_id}", response_model=ResponseModel[List[PromptResponse]])
async def get_category_prompts(category_id: str):
    """获取指定分类的所有提示词"""
    prompts = prompt_manager.get_category_prompts(category_id)
    return ResponseModel(data=prompts)

@router.get("/{prompt_id}", response_model=ResponseModel[PromptResponse])
async def get_prompt(prompt_id: str):
    """获取单个提示词详情"""
    prompt = prompt_manager.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")
    return ResponseModel(data=prompt)

@router.post("/use/{prompt_id}", response_model=ResponseModel[Dict])
async def use_prompt(prompt_id: str):
    """记录提示词使用"""
    success = prompt_manager.increment_use_count(prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="提示词不存在")
    return ResponseModel(data={"message": "success"})

@router.post("/categories", response_model=ResponseModel[Dict])
async def create_category(category: CategoryRequest):
    """创建新分类"""
    success = prompt_manager.create_category(category.dict())
    if not success:
        raise HTTPException(status_code=500, detail="创建分类失败")
    return ResponseModel(data={"message": "success"})

@router.put("/categories/{category_id}", response_model=ResponseModel[Dict])
async def update_category(category_id: str, category: CategoryRequest):
    """更新分类"""
    success = prompt_manager.update_category(category_id, category.dict())
    if not success:
        raise HTTPException(status_code=404, detail="分类不存在")
    return ResponseModel(data={"message": "success"})

@router.post("/", response_model=ResponseModel[Dict])
async def create_prompt(prompt: PromptRequest):
    """创建新提示词"""
    success = prompt_manager.create_prompt(prompt.dict())
    if not success:
        raise HTTPException(status_code=500, detail="创建提示词失败")
    return ResponseModel(data={"message": "success"})

@router.put("/{prompt_id}", response_model=ResponseModel[Dict])
async def update_prompt(prompt_id: str, prompt: PromptRequest):
    """更新提示词"""
    success = prompt_manager.update_prompt(prompt_id, prompt.dict())
    if not success:
        raise HTTPException(status_code=404, detail="提示词不存在")
    return ResponseModel(data={"message": "success"})

@router.delete("/{prompt_id}", response_model=ResponseModel[Dict])
async def delete_prompt(prompt_id: str):
    """删除提示词"""
    success = prompt_manager.delete_prompt(prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="提示词不存在")
    return ResponseModel(data={"message": "success"})

@router.post("/reload", response_model=ResponseModel[Dict])
async def reload_prompts():
    """重新加载预定义的提示词模板"""
    success = prompt_manager.reload_templates()
    if not success:
        raise HTTPException(status_code=500, detail="重新加载提示词模板失败")
    return ResponseModel(data={"message": "success"}) 