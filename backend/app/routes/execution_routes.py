from fastapi import APIRouter, Request
from app.services.code_executor import CodeExecutor

router = APIRouter(tags=["execution"])

# 创建代码执行器实例
code_executor = CodeExecutor()

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