from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any, Optional
from pydantic import BaseModel
import uuid
from app.services.code_executor.note_executor import get_executor

router = APIRouter(prefix="/api/execution", tags=["execution"])

@router.post("/execute")
async def execute_code(request: Request):
    """
    在指定的笔记本中执行代码
    
    Args:
        session_id: 笔记本会话ID
        request: 代码执行请求
        
    Returns:
        执行结果
    """
    try:
        data = await request.json()
        executor = get_executor()
        code = data.get("code", "")
        session_id = data.get("session_id", "")
        result = executor.execute(session_id, code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset_context")
async def reset_context(request: Request):
    """
    重置指定笔记本的执行环境
    
    Args:
        session_id: 笔记本会话ID
    """
    try:
        data = await request.json()
        executor = get_executor()
        session_id = data.get("session_id", "")
        executor = get_executor()
        executor.reset_session(session_id)
        return {"status": "success", "message": "笔记本环境已重置"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
