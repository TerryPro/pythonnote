from fastapi import FastAPI
from app.core.logger import configure_logging
from app.routes import register_routes
from app.core.middlewares import configure_middlewares
from app.core.lifespan import lifespan

def create_app():
    """
    创建并配置 FastAPI 应用实例。

    该函数负责初始化 FastAPI 应用，配置日志、中间件和路由，并设置应用的生命周期管理。

    返回:
        FastAPI: 配置好的 FastAPI 应用实例。
    """
    # 配置日志系统
    configure_logging()
    # 创建 FastAPI 应用实例，并设置生命周期管理
    app = FastAPI(title="DataInsight API", lifespan=lifespan)
    # 配置中间件
    configure_middlewares(app)
    # 注册所有路由
    register_routes(app)
    return app

# 创建应用实例
app = create_app()