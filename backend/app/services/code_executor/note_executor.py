from typing import Dict, Any, Optional
from .session_environment import SessionEnvironment
from app.services.code_executor.dataframe_manager import DataFrameManager

class NoteExecutor:
    """
    笔记本代码执行器，负责管理所有SessionEnvironment实例
    """
    def __init__(self):
        self._sessions: Dict[str, SessionEnvironment] = {}
        self._dataframes: Dict[str, DataFrameManager] = {}
        
    def get_or_create_session(self, session_id: str) -> SessionEnvironment:
        """
        获取或创建一个会话环境
        
        Args:
            session_id: 会话ID，通常对应笔记本ID
            
        Returns:
            SessionEnvironment实例
        """
        if session_id not in self._sessions:
            # 创建新的DataFrameManager实例
            df_manager = DataFrameManager()
            self._dataframes[session_id] = df_manager
            # 创建新的SessionEnvironment实例，并传入DataFrameManager
            self._sessions[session_id] = SessionEnvironment(session_id, df_manager)
        return self._sessions[session_id]
    
    def execute(self, session_id: str, code: str) -> Dict[str, Any]:
        """
        在指定会话中执行代码
        
        Args:
            session_id: 会话ID
            code: 要执行的Python代码
            
        Returns:
            执行结果字典
        """
        print(session_id)
        print(code)
        session = self.get_or_create_session(session_id)
        return session.execute(code)
    
    def reset_session(self, session_id: str):
        """
        重置指定会话的环境
        
        Args:
            session_id: 会话ID
        """
        if session_id in self._sessions:
            self._sessions[session_id].reset()
            self._dataframes[session_id].clear()
            
    def delete_session(self, session_id: str):
        """
        删除指定会话
        
        Args:
            session_id: 会话ID
        """
        if session_id in self._sessions:
            self._sessions[session_id].reset()
            self._dataframes[session_id].clear()
            del self._sessions[session_id]
            del self._dataframes[session_id]
            
    def set_dataframes(self, session_id: str, variables: Dict[str, Any]):
        """
        设置DataFrame变量到指定会话
        
        Args:
            session_id: 会话ID
            variables: 变量字典
        """
        session = self.get_or_create_session(session_id)
        session.set_dataframes(variables)
    
    def get_dataframes(self, session_id: str) -> Dict[str, Any]:
        """
        获取指定会话的所有DataFrame
        
        Args:
            session_id: 会话ID
            
        Returns:
            DataFrame字典
        """
        if session_id in self._dataframes:
            return self._dataframes[session_id].get_dataframes()
        return {}
    
    def get_dataframes_names(self, session_id: str) -> Dict[str, Any]:
        """
        获取指定会话的所有DataFrame的名字
        
        Args:
            session_id: 会话ID
            
        Returns:
            DataFrame名字列表
        """
        if session_id in self._dataframes:
            return self._dataframes[session_id].get_dataframes_names()
        return {}
    
    def get_dataframe(self, session_id: str, name: str) -> Any:
        """
        获取指定会话中的DataFrame
        
        Args:
            session_id: 会话ID
            name: DataFrame变量名
            
        Returns:
            DataFrame对象或None
        """
        if session_id in self._dataframes:
            return self._dataframes[session_id].get_dataframe(name)
        return None
    
    def save_dataframe_to_file(self, session_id: str, name: str, file_path: str, file_type: str, **kwargs) -> Dict[str, Any]:
        """
        保存DataFrame到指定文件
        
        Args:
            session_id: 会话ID
            name: DataFrame变量名
            file_path: 文件路径
            file_type: 文件类型
            **kwargs: 保存选项
        """
        if session_id in self._dataframes:
            return self._dataframes[session_id].save_dataframe(name, file_path, file_type, **kwargs)
        return {}

# 创建单例实例
_executor: Optional[NoteExecutor] = None

def get_executor() -> NoteExecutor:
    """获取NoteExecutor的单例实例"""
    global _executor
    if _executor is None:
        _executor = NoteExecutor()
    return _executor 