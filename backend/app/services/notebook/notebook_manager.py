import json
import os
from pathlib import Path
from app.core.config import settings
from app.services.notebook.notedata_loader import NoteDataLoader
from app.services.code_executor.note_executor import get_executor

class NoteBookManager:
    def __init__(self):
        self.note_data_loader = NoteDataLoader()

    def list_notebooks(self):
        try:
            notebooks = []
            for file in settings.NOTEBOOKS_DIR.glob("*.ipynb"):
                notebooks.append({
                    "name": file.name,
                    "path": file.name,
                    "last_modified": os.path.getmtime(file)
                })
            notebooks.sort(key=lambda x: x["name"])
            return {"status": "success", "data": notebooks}
        except Exception as e:
            return {"status": "error", "message": f"获取笔记本列表失败: {str(e)}"}

    def save_notebook(self, filename: str, notebook: dict):
        if not filename or not notebook:
            return {"status": "error", "message": "Missing filename or notebook data"}
        try:
            file_path = settings.NOTEBOOKS_DIR / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(notebook, f, ensure_ascii=False, indent=2)
            
            session_id = notebook.get("session_id", "")
            code_executor = get_executor()
            variables = code_executor.get_dataframes(session_id)
            
            self.note_data_loader.save_notedata(filename, variables)
            
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": f"保存笔记本失败: {str(e)}"}

    def rename_notebook(self, old_filename: str, new_filename: str):
        if not old_filename or not new_filename:
            return {"status": "error", "message": "Missing old_filename or new_filename"}
        if not new_filename.endswith('.ipynb'):
            return {"status": "error", "message": "New filename must end with .ipynb"}
        
        old_path = settings.NOTEBOOKS_DIR / old_filename
        new_path = settings.NOTEBOOKS_DIR / new_filename
        
        if not old_path.exists():
            return {"status": "error", "message": "Source notebook not found"}
        if new_path.exists():
            return {"status": "error", "message": "A notebook with this name already exists"}
        
        try:
            old_path.rename(new_path)
            self.note_data_loader.rename_notedata(old_filename, new_filename)
            return {"status": "success", "message": "Notebook renamed successfully"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to rename notebook: {str(e)}"}

    def delete_notebook(self, filename: str):
        try:
            file_path = settings.NOTEBOOKS_DIR / filename
            if not file_path.exists():
                return {"status": "error", "message": "笔记本不存在"}
            if not filename.endswith('.ipynb'):
                return {"status": "error", "message": "无效的文件类型"}
            
            file_path.unlink()
            self.note_data_loader.delete_notedata(filename)
            
            return {"status": "success", "message": "笔记本删除成功"}
        except Exception as e:
            return {"status": "error", "message": f"删除笔记本失败: {str(e)}"}

    def load_notebook(self, filename: str):
        file_path = settings.NOTEBOOKS_DIR / filename
        if not file_path.exists():
            return {"status": "error", "message": "Notebook not found"}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                notebook = json.load(f)
            return {"status": "success", "data": notebook}
        except Exception as e:
            return {"status": "error", "message": f"加载笔记本失败: {str(e)}"}

