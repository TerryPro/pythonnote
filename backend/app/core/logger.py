import logging
from app.core.config import settings

def configure_logging():
    """
    配置应用程序的日志系统。

    该函数根据 settings 中的配置初始化日志系统，包括日志级别和日志格式。
    日志级别和格式通过 settings.LOG_LEVEL 和 settings.LOG_FORMAT 配置。

    返回:
        logging.Logger: 配置好的日志记录器实例。
    """
    logging.basicConfig(
        level=settings.LOG_LEVEL,  # 设置日志级别
        format=settings.LOG_FORMAT  # 设置日志格式
    )
    logger = logging.getLogger(__name__)  # 获取当前模块的日志记录器
    return logger