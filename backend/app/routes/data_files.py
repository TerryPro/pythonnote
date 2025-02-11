from fastapi import APIRouter, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import os
import shutil
from typing import List
from pathlib import Path
from app.services.data_explorer.data_loader import DataLoader
from app.core.config import settings

router = APIRouter(prefix="/api/data-files", tags=["data-files"])

# 创建数据加载器实例
data_loader = DataLoader()

@router.get("/list")
async def list_data_files():
    """列出所有数据文件"""
    try:
        files = []
        for file in settings.DATA_DIR.glob("*"):
            if file.suffix.lower() in ['.csv', '.xlsx', '.xls']:
                files.append({
                    "name": file.name,
                    "path": str(file.relative_to(settings.DATA_DIR)),
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
        file_path = settings.DATA_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        if not str(file_path.absolute()).startswith(str(settings.DATA_DIR.absolute())):
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

@router.post("/rename")
async def rename_data_file(request: Request):
    """重命名数据文件"""
    try:
        data = await request.json()
        old_filename = data.get("old_filename")
        new_filename = data.get("new_filename")
        
        if not old_filename or not new_filename:
            raise HTTPException(status_code=400, detail="缺少旧文件名或新文件名")
        
        # 构建文件路径
        old_path = settings.DATA_DIR / old_filename
        new_path = settings.DATA_DIR / new_filename
        
        # 检查源文件是否存在
        if not old_path.exists():
            raise HTTPException(status_code=404, detail="源文件不存在")
        
        # 检查新文件名是否已存在
        if new_path.exists():
            raise HTTPException(status_code=400, detail="目标文件名已存在")
        
        # 检查文件扩展名
        old_ext = old_path.suffix.lower()
        new_ext = new_path.suffix.lower()
        if old_ext != new_ext:
            raise HTTPException(status_code=400, detail="不允许更改文件扩展名")
        
        # 检查文件扩展名是否支持
        if new_ext not in ['.csv', '.xlsx', '.xls']:
            raise HTTPException(status_code=400, detail="不支持的文件格式")
        
        # 重命名文件
        old_path.rename(new_path)
        
        return {
            "status": "success",
            "message": "文件重命名成功",
            "data": {
                "old_path": str(old_path.relative_to(settings.DATA_DIR)),
                "new_path": str(new_path.relative_to(settings.DATA_DIR))
            }
        }
    except HTTPException as e:
        raise e
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
        file_path = settings.DATA_DIR / safe_filename
        
        # 如果文件已存在，添加数字后缀
        counter = 1
        while file_path.exists():
            stem = Path(file.filename).stem
            file_path = settings.DATA_DIR / f"{stem}_{counter}{file_ext}"
            counter += 1
        
        # 保存文件
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "status": "success",
            "message": "文件上传成功",
            "data": {
                "file_path": str(file_path.relative_to(settings.DATA_DIR)),
                "file_name": file_path.name,
                "file_size": file_path.stat().st_size
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 