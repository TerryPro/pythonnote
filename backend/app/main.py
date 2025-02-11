from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
import os
import logging
from pathlib import Path
from app.services.code_executor import CodeExecutor
from app.services.pdf.code_formatter import format_python_code
from app.services.pdf.exporter import NotebookPDFExporter
from app.routes import data_explorer, data_files, ai_routes, dataframe_routes, prompt_routes, example_routes
from app.routes.dataframe_routes import router as dataframe_router
from app.routes.prompt_routes import router as prompt_router
from app.routes.example_routes import router as example_router
from app.routes.notebook_routes import router as notebook_router
from app.routes.execution_routes import router as execution_router
from app.routes.export_routes import router as export_router
from app.routes.system_routes import router as system_router
from app.core.config import settings

# 配置日志
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用程序生命周期管理
    """
    # 启动时的操作
    logger.info("服务启动...")
    # 检查环境变量
    if not settings.DEEPSEEK_API_KEY:
        logger.warning("DEEPSEEK_API_KEY 环境变量未设置")
    # 创建必要的目录
    settings.setup_directories()
    logger.info("服务启动完成")
    
    yield  # 服务运行期间
    
    # 关闭时的操作
    logger.info("应用程序关闭...")

app = FastAPI(title=settings.API_TITLE, lifespan=lifespan)
code_executor = CodeExecutor()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    **settings.cors_settings
)

# 创建PDF导出器实例
pdf_exporter = NotebookPDFExporter(settings.EXPORT_DIR)

# 注册路由
logger.info("注册路由...")
app.include_router(system_router)  # 系统路由放在最前面
app.include_router(data_explorer.router)
app.include_router(data_files.router)
app.include_router(ai_routes.router)
app.include_router(dataframe_router)
app.include_router(prompt_router)
app.include_router(example_router)
app.include_router(notebook_router)
app.include_router(execution_router)
app.include_router(export_router)
logger.info("路由注册完成")

@app.post("/execute")
async def execute_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    result = code_executor.execute(code)
    return result

@app.post("/reset_context")
async def reset_context():
    code_executor.reset()
    return {"status": "success"}

@app.post("/export_pdf")
async def export_pdf(request: Request):
    try:
        data = await request.json()
        notebook = data.get("notebook", {})
        filename = data.get("filename", "notebook.pdf")
        
        # 使用PDF导出器生成PDF文件
        pdf_path = pdf_exporter.export(notebook, filename)
        
        # 返回生成的PDF文件
        return FileResponse(
            path=str(pdf_path),
            media_type='application/pdf',
            filename=filename
        )
        
    except Exception as e:
        print(f"PDF导出错误: {str(e)}")  # 添加错误日志
        raise HTTPException(status_code=500, detail=str(e)) 

@app.get("/")
async def root():
    logger.info("访问根路径")
    return {"message": "Welcome to AI Code Generator API"} 

@app.get("/api/version")
async def get_version():
    """获取系统版本信息"""
    try:
        return {
            "status": "success",
            "data": settings.VERSION
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 