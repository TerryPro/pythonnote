from fastapi import FastAPI
from app.routes.dataframe_routes import router as dataframe_router
from app.routes.prompt_routes import router as prompt_router
from app.routes.example_routes import router as example_router
from app.routes.notebook_routes import router as notebook_router
from app.routes.execution_routes import router as execution_router
from app.routes.export_routes import router as export_router
from app.routes.system_routes import router as system_router
from app.routes.data_explorer import router as data_explorer_router
from app.routes.data_files import router as data_files_router
from app.routes.ai_routes import router as ai_router
import logging

logger = logging.getLogger(__name__)  # 获取当前模块的日志记录器

def register_routes(app: FastAPI):
    """
    注册所有路由到 FastAPI 应用。

    该函数将所有子模块的路由器（router）注册到主应用中，并记录注册过程。
    每个路由器的注册顺序决定了其在 API 文档中的显示顺序。

    参数:
        app (FastAPI): FastAPI 应用实例。
    """
    logger.info("注册路由...")
    # 注册系统相关路由
    app.include_router(system_router)
    # 注册数据探索相关路由
    app.include_router(data_explorer_router)
    # 注册数据文件管理相关路由
    app.include_router(data_files_router)
    # 注册 AI 功能相关路由
    app.include_router(ai_router)
    # 注册数据框操作相关路由
    app.include_router(dataframe_router)
    # 注册提示词管理相关路由
    app.include_router(prompt_router)
    # 注册示例相关路由
    app.include_router(example_router)
    # 注册笔记本相关路由
    app.include_router(notebook_router)
    # 注册执行相关路由
    app.include_router(execution_router)
    # 注册导出相关路由
    app.include_router(export_router)
    logger.info("路由注册完成")