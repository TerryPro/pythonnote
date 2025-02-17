import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings

logger = logging.getLogger(__name__)

async def startup_event():
    """服务启动事件"""
    logger.info("服务启动...")
    if not settings.DEEPSEEK_API_KEY:
        logger.warning("DEEPSEEK_API_KEY 环境变量未设置")
    settings.setup_directories()
    logger.info("服务启动完成")

async def shutdown_event():
    """服务关闭事件"""
    logger.info("应用程序关闭...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """生命周期管理"""
    await startup_event()
    yield
    await shutdown_event()