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
from app.services.code_executor.dataframe_manager import DataFrameManager

# 过滤掉特定的警告
warnings.filterwarnings('ignore', category=UserWarning, message='FigureCanvasAgg is non-interactive')

class SessionEnvironment:
    """
    为每个笔记提供一个隔离的Python执行环境
    """
    def __init__(self, session_id: str, df_manager: DataFrameManager):
        """
        初始化会话环境
        
        Args:
            session_id: 会话ID，通常对应笔记本ID
            df_manager: DataFrame管理器实例
        """
        self.session_id = session_id
        self.df_manager = df_manager
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
            
            try:
                plot_data = self._last_plotly_fig.to_json()
                plot_data = plot_data.replace('True', 'true').replace('False', 'false')
                
                plot_layout = self._last_plotly_fig.layout.to_plotly_json()
                plot_layout = str(plot_layout).replace('True', 'true').replace('False', 'false')
            except Exception:
                import json
                plot_data = json.dumps(self._last_plotly_fig.data)
                plot_layout = json.dumps(self._last_plotly_fig.layout)
                plot_data = plot_data.replace('True', 'true').replace('False', 'false')
                plot_layout = plot_layout.replace('True', 'true').replace('False', 'false')
            
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
                            layout.height = null;
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
            
            self._last_plotly_fig = None
            return html
            
        except Exception:
            return ''

    def execute(self, code: str) -> Dict[str, Any]:
        """
        在当前会话环境中执行Python代码
        
        Args:
            code: 要执行的Python代码
            
        Returns:
            Dict包含执行结果
        """
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        result = {
            "output": "",
            "error": None,
            "status": "success",
            "has_dataframes": False,
            "plot": "",
            "plotly_html": ""
        }
        
        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exec(code, self.globals_dict, self.locals_dict)
                
            self._register_dataframes()
            result["has_dataframes"] = len(self.df_manager.get_dataframes_names()) > 0
            
            result["plot"] = self._capture_plot()
            result["plotly_html"] = self._capture_plotly()
            
            output = stdout.getvalue()
            errors = stderr.getvalue()
            
            if errors:
                result["error"] = errors
                result["status"] = "error"
            
            result["output"] = output if output else errors
            
        except Exception:
            error_msg = traceback.format_exc()
            result["error"] = str(error_msg)
            result["status"] = "error"
            result["output"] = error_msg
        
        finally:
            stdout.close()
            stderr.close()
        
        return result

    def reset(self):
        """重置会话环境状态"""
        plt.close('all')
        self._last_plotly_fig = None
        self._show_called = False
        
        # 清除当前会话的DataFrame对象
        self.df_manager.clear()
        
        # 初始化命名空间
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
        
        # 添加内置函数
        for name in dir(builtins):
            if not name.startswith('_'):
                self.globals_dict[name] = getattr(builtins, name)
                
        plt.switch_backend('Agg')
        plt.ioff()
        plt.rcParams['figure.max_open_warning'] = 50
        plt.rcParams['figure.dpi'] = 100

        def custom_show(*args, **kwargs):
            self._show_called = True
            return None
        
        plt.show = custom_show

        def custom_plotly_show(fig, *args, **kwargs):
            self._last_plotly_fig = fig
            return None
        
        plotly.io.show = custom_plotly_show

    def set_dataframes(self, variables: Dict[str, Any]):
        """设置DataFrame变量到当前会话"""
        self.locals_dict.update(variables)
        for var_name, var_value in self.locals_dict.items():
            if isinstance(var_value, pd.DataFrame):
                self.df_manager.register_dataframe(var_name, var_value)
                
    def get_dataframes(self):
        """获取当前会话的所有DataFrame"""
        return self.df_manager.get_dataframes()
    
    def _register_dataframes(self):
        """注册所有DataFrame变量到管理器"""
        for var_name, var_value in self.locals_dict.items():
            if isinstance(var_value, pd.DataFrame):
                self.df_manager.register_dataframe(var_name, var_value)
        
        for var_name, var_value in self.globals_dict.items():
            if var_name.startswith('__') or isinstance(var_value, type(pd)):
                continue
            if isinstance(var_value, pd.DataFrame):
                self.df_manager.register_dataframe(var_name, var_value) 