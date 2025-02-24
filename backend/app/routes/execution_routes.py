from fastapi import APIRouter, Request
from app.services.code_executor.code_executor import get_executor

router = APIRouter(prefix="/api/execution", tags=["execution"])

# 创建代码执行器实例
code_executor = get_executor()

@router.post("/execute")
async def execute_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    result = code_executor.execute(code)
    return result

@router.post("/reset_context")
async def reset_context():
    code_executor.reset()
    return {"status": "success"} 