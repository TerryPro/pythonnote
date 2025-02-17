'''
API 服务层，封装了根消息和版本信息的获取逻辑
'''

from app.core.version import VERSION


def get_root_message() -> dict:
    """
    获取根消息
    """
    return {"status": "success", "data": "Welcome to AI Data Analysis API"}


def get_version_info() -> dict:
    """
    获取系统版本信息
    """
    try:
        return {"status": "success", "data": VERSION}
    except Exception as e:
        return {"status": "error", "detail": str(e)} 
    