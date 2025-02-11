"""
代码执行器服务模块

该模块提供了Python代码的执行环境，包括：
- 代码执行和结果捕获
- matplotlib图形输出支持
- plotly图形输出支持
- DataFrame变量管理
"""

from .code_executor import CodeExecutor

__all__ = ['CodeExecutor'] 