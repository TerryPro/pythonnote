from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from typing import List
from pathlib import Path
from services.data_explorer.data_loader import DataLoader

router = APIRouter(prefix="/api/data-files", tags=["data-files"])

# 配置数据文件存储目录
DATA_DIR = Path("data")
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)

# 创建数据加载器实例
data_loader = DataLoader()

@router.get("/list")
async def list_data_files():
    """列出所有数据文件"""
    try:
        files = []
        for file in DATA_DIR.glob("*"):
            if file.suffix.lower() in ['.csv', '.xlsx', '.xls']:
                files.append({
                    "name": file.name,
                    "path": str(file.relative_to(DATA_DIR)),
                    "size": file.stat().st_size,
                    "modified": file.stat().st_mtime
                })
        return {"status": "success", "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
async def delete_data_file(filename: str):
    """删除指定的数据文件"""
    try:
        file_path = DATA_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        if not str(file_path.absolute()).startswith(str(DATA_DIR.absolute())):
            raise HTTPException(status_code=400, detail="非法的文件路径")
        
        os.remove(file_path)
        return {"status": "success", "message": "文件删除成功"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload/csv")
async def upload_csv(file: UploadFile):
    """上传CSV文件"""
    return await save_data_file(file, ['.csv'])

@router.post("/upload/excel")
async def upload_excel(file: UploadFile):
    """上传Excel文件"""
    return await save_data_file(file, ['.xlsx', '.xls'])

@router.get("/preview/csv")
async def preview_csv(filename: str):
    """预览CSV文件"""
    try:
        result = data_loader.load_csv(filename)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preview/excel")
async def preview_excel(filename: str, sheet_name: str = None):
    """预览Excel文件"""
    try:
        result = data_loader.load_excel(filename, sheet_name)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def save_data_file(file: UploadFile, allowed_extensions: List[str]):
    """保存数据文件的通用函数"""
    try:
        # 检查文件扩展名
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的文件格式。支持的格式：{', '.join(allowed_extensions)}"
            )
        
        # 生成安全的文件名
        safe_filename = Path(file.filename).name
        file_path = DATA_DIR / safe_filename
        
        # 如果文件已存在，添加数字后缀
        counter = 1
        while file_path.exists():
            stem = Path(file.filename).stem
            file_path = DATA_DIR / f"{stem}_{counter}{file_ext}"
            counter += 1
        
        # 保存文件
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "status": "success",
            "message": "文件上传成功",
            "data": {
                "file_path": str(file_path.relative_to(DATA_DIR)),
                "file_name": file_path.name,
                "file_size": file_path.stat().st_size
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 