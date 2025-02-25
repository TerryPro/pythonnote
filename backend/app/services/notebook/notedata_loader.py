import pickle
from pathlib import Path
from typing import Dict, Any
from app.core.config import settings

class NoteDataLoader:
    """Python笔记本执行环境管理器"""
    
    def __init__(self):
        """初始化环境管理器"""
        self.env_dir = settings.NOTEDATAS_DIR
        self.env_dir.mkdir(exist_ok=True)
    
    def _get_data_path(self, notebook_name: str) -> Path:
        """
        获取环境文件路径
        
        Args:
            notebook_name: 笔记本文件名
            
        Returns:
            Path: 环境文件路径
        """
        # 将.ipynb替换为.dat
        env_name = notebook_name.replace('.ipynb', '.dat')
        return self.env_dir / env_name
    
    def save_notedata(self, notebook_name: str, variables: Dict[str, Any]) -> bool:
        """
        保存Python执行环境
        
        Args:
            notebook_name: 笔记本文件名
            variables: 要保存的变量字典
            
        Returns:
            bool: 保存是否成功
        """
        try:
            env_path = self._get_data_path(notebook_name)
            
            print(env_path)
            
            # 过滤掉不能序列化的对象
            serializable_vars = {}
            for name, value in variables.items():
                try:
                    # 尝试序列化，如果失败则跳过该变量
                    pickle.dumps(value)
                    serializable_vars[name] = value
                except:
                    continue
            
            # 保存环境变量
            with open(env_path, 'wb') as f:
                pickle.dump(serializable_vars, f)
            return True
        except Exception as e:
            print(f"保存执行环境失败: {str(e)}")
            return False
    
    def load_notedata(self, notebook_name: str) -> Dict[str, Any]:
        """
        加载Python执行环境
        
        Args:
            notebook_name: 笔记本文件名
            
        Returns:
            Dict[str, Any]: 加载的变量字典
        """
        try:
            env_path = self._get_data_path(notebook_name)
            
            if not env_path.exists():
                return {}
            
            with open(env_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"加载执行环境失败: {str(e)}")
            return {}
    
    def delete_notedata(self, notebook_name: str) -> bool:
        """
        删除Python执行环境文件
        
        Args:
            notebook_name: 笔记本文件名
            
        Returns:
            bool: 删除是否成功
        """
        try:
            env_path = self._get_data_path(notebook_name)
            if env_path.exists():
                env_path.unlink()
            return True
        except Exception as e:
            print(f"删除执行环境失败: {str(e)}")
            return False
    
    def rename_notedata(self, old_name: str, new_name: str) -> bool:
        """
        重命名Python执行环境文件
        
        Args:
            old_name: 原笔记本文件名
            new_name: 新笔记本文件名
            
        Returns:
            bool: 重命名是否成功
        """
        try:
            old_path = self._get_data_path(old_name)
            new_path = self._get_data_path(new_name)
            
            if old_path.exists():
                old_path.rename(new_path)
            return True
        except Exception as e:
            print(f"重命名执行环境失败: {str(e)}")
            return False 