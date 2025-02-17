from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def configure_middlewares(app: FastAPI):
    """配置中间件"""
    app.add_middleware(
        CORSMiddleware,
        **settings.cors_settings
    )