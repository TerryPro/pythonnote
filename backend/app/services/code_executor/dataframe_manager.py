from typing import Dict, List, Optional, Any
import pandas as pd
from app.core.config import settings

class DataFrameManager:
    """DataFrame变量管理器"""
    
    def __init__(self):
        self._dataframes: Dict[str, pd.DataFrame] = {}
        self._dataframe_info: Dict[str, Dict] = {}
        # 添加数据目录
        self.data_dir = settings.DATA_DIR
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True)
    
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
    
    def get_dataframes_names(self) -> List[str]:
        """
        获取所有已注册的DataFrame变量名
        
        Returns:
            List[str]: 所有DataFrame变量名列表
        """
        return list(self._dataframes.keys())
    
    def get_dataframes(self):
        return self._dataframes
    
    def clear(self):
        """清空所有注册的DataFrame信息"""
        self._dataframes.clear()
        self._dataframe_info.clear()
    
    def save_dataframe(self, name: str, file_path: str, file_type: str = "csv", **save_options) -> Dict[str, Any]:
        """
        保存DataFrame到文件
        
        Args:
            name: DataFrame变量名
            file_path: 保存的文件路径（相对于data目录）
            file_type: 文件类型，支持 "csv" 和 "excel"
            save_options: 保存选项，将直接传递给pandas的to_csv或to_excel方法
            
        Returns:
            Dict[str, Any]: 包含保存结果的信息
            
        Raises:
            ValueError: 当DataFrame不存在或保存失败时
        """
        df = self.get_dataframe(name)
        if df is None:
            raise ValueError(f"DataFrame '{name}' 不存在")
            
        try:
            # 确保文件路径是相对于data目录的
            full_path = self.data_dir / file_path
            
            # 确保父目录存在
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 根据文件类型选择保存方法
            if file_type.lower() == "csv":
                # 设置默认的CSV保存选项
                default_options = {
                    "index": False,
                    "encoding": "utf-8"
                }
                # 更新选项
                save_options = {**default_options, **save_options}
                df.to_csv(full_path, **save_options)
            elif file_type.lower() == "excel":
                # 设置默认的Excel保存选项
                default_options = {
                    "index": False,
                    "engine": "openpyxl"
                }
                # 更新选项
                save_options = {**default_options, **save_options}
                df.to_excel(full_path, **save_options)
            else:
                raise ValueError(f"不支持的文件类型: {file_type}")
                
            # 返回保存结果信息
            return {
                "status": "success",
                "message": f"DataFrame '{name}' 已成功保存到 {file_path}",
                "file_info": {
                    "file_path": str(file_path),
                    "file_type": file_type,
                    "file_size": f"{full_path.stat().st_size / 1024:.2f} KB",
                    "save_time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
        except Exception as e:
            raise ValueError(f"保存DataFrame失败: {str(e)}") 