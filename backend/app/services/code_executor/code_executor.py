import sys
import io
from typing import Dict, Any, Optional
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
from app.services.data_explorer.data_loader import get_manager

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
        if plt.get_fignums():  # 只要有图形就捕获
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

    def execute(self, code: str) -> Dict[str, Any]:
        """
        执行Python代码
        
        Args:
            code: 要执行的Python代码
            
        Returns:
            Dict包含执行结果：
            {
                "output": str,  # 标准输出和错误
                "error": Optional[str],  # 如果有错误，则包含错误信息
                "status": str  # 执行状态：'success' 或 'error'
            }
        """
        
        # 捕获标准输出和错误
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        result = {
            "output": "",
            "error": None,
            "status": "success",
            "has_dataframes": False,  # 添加标志位表示是否有新的DataFrame变量
            "plot": "",  # 添加matplotlib图像输出
            "plotly_html": ""  # 添加plotly图像输出
        }
        
        try:
            # 执行代码并捕获输出
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exec(code, self.globals_dict, self.locals_dict)
                
            # 清空已注册的DataFrame变量
            get_manager().clear()
            # 注册所有DataFrame变量
            self._register_dataframes()
            # 检查是否有DataFrame变量
            result["has_dataframes"] = len(get_manager().get_all_dataframes()) > 0
            
            # 捕获matplotlib图像
            result["plot"] = self._capture_plot()
            # 捕获plotly图像
            result["plotly_html"] = self._capture_plotly()
            
            # 获取输出
            output = stdout.getvalue()
            errors = stderr.getvalue()
            
            if errors:
                result["error"] = errors
                result["status"] = "error"
            
            result["output"] = output if output else errors
            
        except Exception as e:
            # 获取完整的错误追踪
            error_msg = traceback.format_exc()
            result["error"] = str(error_msg)
            result["status"] = "error"
            result["output"] = error_msg
        
        finally:
            stdout.close()
            stderr.close()
        
        return result

    def reset(self):
        """重置执行器状态"""
        # 清除所有图形
        plt.close('all')
        self._last_plotly_fig = None
        self._show_called = False  # 添加标志
        
        # 清除所有已注册的DataFrame对象
        manager = get_manager()
        manager.clear()
        
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

    def _register_dataframes(self):
        """注册所有DataFrame变量到管理器"""
        manager = get_manager()
        
        # 遍历所有局部变量
        for var_name, var_value in self.locals_dict.items():
            if isinstance(var_value, pd.DataFrame):
                manager.register_dataframe(var_name, var_value)
        
        # 遍历所有全局变量
        for var_name, var_value in self.globals_dict.items():
            # 跳过模块和内置变量
            if var_name.startswith('__') or isinstance(var_value, type(pd)):
                continue
            if isinstance(var_value, pd.DataFrame):
                manager.register_dataframe(var_name, var_value) 