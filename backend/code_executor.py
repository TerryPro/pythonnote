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
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import warnings
from contextlib import redirect_stdout, redirect_stderr
import base64
from io import BytesIO
import uuid

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
        # 设置plotly的默认模板
        pio.templates.default = "plotly_white"
        self.reset()
                
    def _capture_plot(self) -> str:
        """捕获matplotlib图形并转换为base64字符串"""
        if plt.get_fignums() and hasattr(self, '_show_called') and self._show_called:
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close()  # 清除当前图形
            buf.seek(0)
            self._show_called = False  # 重置标志
            return f'<img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}">'
        return ''

    def _capture_plotly(self) -> str:
        """捕获最后一个plotly图形并转换为HTML"""
        if not hasattr(self, '_last_plotly_fig') or self._last_plotly_fig is None:
            return ''
            
        try:
            # 配置输出选项，使用小写的 true/false
            config = {
                'displayModeBar': 'true',
                'responsive': 'true',
                'scrollZoom': 'true',
                'showLink': 'false',
                'displaylogo': 'false',
                'modeBarButtonsToRemove': ['sendDataToCloud'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'plotly_graph',
                    'height': 500,
                    'width': 700,
                    'scale': 2
                }
            }
            
            # 准备图表数据
            try:
                plot_data = self._last_plotly_fig.to_json()
                # 替换 Python 的布尔值为 JavaScript 的布尔值
                plot_data = plot_data.replace('True', 'true').replace('False', 'false')
                
                plot_layout = self._last_plotly_fig.layout.to_plotly_json()
                # 替换 Python 的布尔值为 JavaScript 的布尔值
                plot_layout = str(plot_layout).replace('True', 'true').replace('False', 'false')
            except Exception as e:
                import json
                plot_data = json.dumps(self._last_plotly_fig.data)
                plot_layout = json.dumps(self._last_plotly_fig.layout)
                # 替换 Python 的布尔值为 JavaScript 的布尔值
                plot_data = plot_data.replace('True', 'true').replace('False', 'false')
                plot_layout = plot_layout.replace('True', 'true').replace('False', 'false')
            
            # 构建HTML
            html = f'''
            <div class="plotly-graph-div" style="height:100%; width:100%;">
            <script type="text/javascript">
                (function() {{
                    if (window.Plotly) {{
                        try {{
                            var data = {plot_data};
                            var layout = {plot_layout};
                            layout.autosize = true;
                            layout.margin = {{ t: 30, r: 10, b: 30, l: 60 }};
                            layout.height = null; // 让高度自适应容器
                            var config = {config};
                            
                            var container = document.currentScript.parentElement;
                            Plotly.newPlot(container, data, layout, config)
                                .then(function() {{
                                    window.dispatchEvent(new Event('resize'));
                                }});
                        }} catch(e) {{
                            console.error("[Plotly] 初始化错误:", e);
                        }}
                    }}
                }})();
            </script>
            </div>
            '''
            
            # 清除存储的图形
            self._last_plotly_fig = None
            return html
            
        except Exception as e:
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
                - plot: 如果有matplotlib图形输出，包含base64编码的图像
                - plotly_html: 如果有plotly图形输出，包含HTML
        """
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        result = {
            'status': 'success',
            'output': '',
            'error': None,
            'plot': None,
            'plotly_html': None
        }
        
        # 重置上一个plotly图形
        self._last_plotly_fig = None
        
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
                
            # 捕获matplotlib图形输出
            plot_output = self._capture_plot()
            if plot_output:
                result['plot'] = plot_output

            # 捕获plotly图形输出
            plotly_output = self._capture_plotly()
            if plotly_output:
                result['plotly_html'] = plotly_output
                
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
        self._last_plotly_fig = None
        self._show_called = False  # 添加标志
        
        # 初始化全局和局部命名空间
        self.globals_dict = {
            '__name__': '__main__',
            'np': np,
            'pd': pd,
            'plt': plt,
            'px': px,
            'go': go,
            'plotly': plotly
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

        # 重写 plt.show 函数来跟踪调用
        def custom_show(*args, **kwargs):
            self._show_called = True
            return None
        
        plt.show = custom_show

        # 重写plotly的show函数来捕获图形
        def custom_plotly_show(fig, *args, **kwargs):
            self._last_plotly_fig = fig
            return None
        
        plotly.io.show = custom_plotly_show 