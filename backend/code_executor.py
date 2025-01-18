import sys
import io
from typing import Dict, Any
import traceback
import builtins
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 在导入plt之前设置后端
import matplotlib.pyplot as plt
import warnings
from contextlib import redirect_stdout, redirect_stderr
import base64
from io import BytesIO

# 过滤掉特定的警告
warnings.filterwarnings('ignore', category=UserWarning, message='FigureCanvasAgg is non-interactive')

class CodeExecutor:
    def __init__(self):
        # 设置matplotlib的全局配置
        plt.ioff()  # 确保关闭交互模式
        plt.rcParams.update({
            'figure.max_open_warning': 50,
            'figure.dpi': 100,
            'interactive': False
        })
        self.reset()
                
    def _capture_plot(self) -> str:
        """捕获matplotlib图形并转换为base64字符串"""
        if plt.get_fignums():
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close()  # 清除当前图形
            buf.seek(0)
            return f'<img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}">'
        return ''
        
    def execute(self, code: str) -> dict:
        """执行代码并返回结果
        
        Args:
            code: 要执行的代码字符串
            
        Returns:
            dict: 包含执行结果的字典，包括：
                - status: 执行状态 ('success' 或 'error')
                - output: 标准输出和错误输出
                - error: 如果发生错误，包含错误详情
                - plot: 如果有图形输出，包含base64编码的图像
        """
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        result = {
            'status': 'success',
            'output': '',
            'error': None,
            'plot': None
        }
        
        try:
            # 重定向标准输出和错误
            with redirect_stdout(stdout), redirect_stderr(stderr):
                # 编译代码
                compiled_code = compile(code, '<string>', 'exec')
                # 执行代码
                exec(compiled_code, self.globals_dict, self.locals_dict)
            
            # 获取输出
            output = stdout.getvalue()
            if output:
                result['output'] = output
                
            # 捕获错误输出
            error_output = stderr.getvalue()
            if error_output:
                result['output'] += f'\n{error_output}'
                
            # 捕获图形输出
            plot_output = self._capture_plot()
            if plot_output:
                result['plot'] = plot_output
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = {
                'type': type(e).__name__,
                'message': str(e),
                'traceback': traceback.format_exc()
            }
        
        return result
        
    def reset(self):
        """完全重置执行器状态"""
        # 清除所有图形
        plt.close('all')
        
        # 初始化全局和局部命名空间
        self.globals_dict = {
            '__name__': '__main__',
            'np': np,
            'pd': pd,
            'plt': plt,
        }
        self.locals_dict = {}
        
        # 添加所有内置函数到全局命名空间
        for name in dir(builtins):
            if not name.startswith('_'):
                self.globals_dict[name] = getattr(builtins, name)
                
        # 设置matplotlib为内联模式并禁用警告
        plt.switch_backend('Agg')
        plt.ioff()  # 关闭交互模式
        # 设置图形显示参数
        plt.rcParams['figure.max_open_warning'] = 50
        plt.rcParams['figure.dpi'] = 100 