import pandas as pd
from typing import Optional, Dict, List, Any
import os
from pathlib import Path

class DataLoadError(Exception):
    """数据加载错误的自定义异常类"""
    pass

class DataLoader:
    """数据加载和预处理类"""
    
    def __init__(self):
        """初始化DataLoader"""
        self.current_data: Optional[pd.DataFrame] = None
        self.data_info: Optional[Dict] = None
        self.file_info: Optional[Dict] = None
        self.data_dir = Path("data")
    
    def load_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """加载pandas DataFrame数据
        
        Args:
            df: 要加载的pandas DataFrame对象
            
        Returns:
            Dict包含数据预览信息：
            {
                "head": 前5行数据,
                "info": 数据基本信息,
                "summary": 数据统计摘要
            }
        
        Raises:
            DataLoadError: 当DataFrame为空或格式不正确时
        """
        if df is None or df.empty:
            raise DataLoadError("DataFrame不能为空")
            
        self.current_data = df
        self._update_data_info()
        return self.get_preview()
    
    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """获取文件基本信息"""
        return {
            "文件名": file_path.name,
            "文件大小": f"{file_path.stat().st_size / 1024:.2f} KB",
            "最后修改时间": pd.Timestamp(file_path.stat().st_mtime, unit='s').strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def load_csv(self, file_path: str, encoding: str = 'utf-8', sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """加载CSV文件"""
        file_path = self.data_dir / file_path
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        if file_path.stat().st_size == 0:
            raise ValueError("文件为空")
        
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            result = self.load_dataframe(df)
            result["file_info"] = self._get_file_info(file_path)
            return result
        except Exception as e:
            raise ValueError(f"CSV文件解析错误: {str(e)}")
    
    def load_excel(self, file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """加载Excel文件"""
        file_path = self.data_dir / file_path
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        if file_path.stat().st_size == 0:
            raise ValueError("文件为空")
        
        try:
            # 如果没有指定sheet_name，读取第一个sheet
            if sheet_name is None:
                # 获取所有sheet名称
                excel_file = pd.ExcelFile(file_path)
                sheet_names = excel_file.sheet_names
                if not sheet_names:
                    raise ValueError("Excel文件中没有工作表")
                sheet_name = sheet_names[0]
            
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            result = self.load_dataframe(df)
            file_info = self._get_file_info(file_path)
            file_info["工作表"] = sheet_name
            result["file_info"] = file_info
            return result
        except Exception as e:
            raise ValueError(f"Excel文件解析错误: {str(e)}")
    
    def _update_data_info(self) -> None:
        """更新数据信息"""
        if self.current_data is not None:
            self.data_info = {
                "行数": len(self.current_data),
                "列数": len(self.current_data.columns),
                "列名": list(self.current_data.columns),
                "数据类型": {str(k): str(v) for k, v in self.current_data.dtypes.items()},
                "内存占用": f"{self.current_data.memory_usage().sum() / 1024**2:.2f} MB",
                "空值统计": self.current_data.isnull().sum().to_dict()
            }
    
    def get_preview(self, rows: int = 5) -> Optional[Dict[str, Any]]:
        """获取数据预览
        
        Args:
            rows: 预览的行数，默认5行
            
        Returns:
            包含预览信息的字典，如果没有数据则返回None
        """
        if self.current_data is None:
            return None
            
        return {
            "head": self.current_data.head(rows).to_dict('records'),
            "info": self.data_info,
            "summary": self.current_data.describe().to_dict()
        } 

"""
DataFrame变量管理服务
"""
from typing import Dict, List, Optional
import pandas as pd

class DataFrameManager:
    """DataFrame变量管理器"""
    
    def __init__(self):
        self._dataframes: Dict[str, pd.DataFrame] = {}
        self._dataframe_info: Dict[str, Dict] = {}
    
    def register_dataframe(self, name: str, df: pd.DataFrame) -> None:
        """
        注册一个DataFrame变量并更新其信息
        
        Args:
            name: DataFrame变量名
            df: DataFrame对象
        """
        self._dataframes[name] = df
        self._update_dataframe_info(name)
    
    def _update_dataframe_info(self, name: str) -> None:
        """
        更新指定DataFrame的信息
        
        Args:
            name: DataFrame变量名
        """
        df = self._dataframes.get(name)
        if df is not None:
            self._dataframe_info[name] = {
                "basic_info": {
                    "行数": len(df),
                    "列数": len(df.columns),
                    "内存占用": f"{df.memory_usage().sum() / 1024**2:.2f} MB"
                },
                "columns": [
                    {
                        "name": str(col),
                        "type": str(df[col].dtype),
                        "null_count": int(df[col].isnull().sum())
                    }
                    for col in df.columns
                ],
                "preview": {
                    "head": df.head().to_dict('records'),
                    "summary": df.describe().to_dict()
                }
            }
    
    def get_dataframe(self, name: str) -> Optional[pd.DataFrame]:
        """
        获取指定名称的DataFrame对象
        
        Args:
            name: DataFrame变量名
            
        Returns:
            Optional[pd.DataFrame]: DataFrame对象，如果不存在则返回None
        """
        return self._dataframes.get(name)
    
    def get_dataframe_info(self, name: str) -> Optional[Dict]:
        """
        获取指定DataFrame的详细信息
        
        Args:
            name: DataFrame变量名
            
        Returns:
            Optional[Dict]: DataFrame的详细信息，如果不存在则返回None
        """
        if name not in self._dataframe_info:
            self._update_dataframe_info(name)
        return self._dataframe_info.get(name)
    
    def get_all_dataframes(self) -> List[str]:
        """
        获取所有已注册的DataFrame变量名
        
        Returns:
            List[str]: 所有DataFrame变量名列表
        """
        return list(self._dataframes.keys())
    
    def clear(self):
        """清空所有注册的DataFrame信息"""
        self._dataframes.clear()
        self._dataframe_info.clear()

# 创建单例实例
_manager: Optional[DataFrameManager] = None

def get_manager() -> DataFrameManager:
    """获取DataFrameManager的单例实例"""
    global _manager
    if _manager is None:
        _manager = DataFrameManager()
    return _manager 