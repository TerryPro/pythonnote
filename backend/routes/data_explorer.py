from fastapi import APIRouter, UploadFile, File, HTTPException
from services.data_explorer.data_loader import DataLoader, DataLoadError
import tempfile
import os
from typing import Dict, Any

# 创建路由器，设置前缀
router = APIRouter(prefix="/api/data-explorer", tags=["data-explorer"])

# 创建数据加载器实例
data_loader = DataLoader()

@router.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...)) -> Dict[str, Any]:
    """处理CSV文件上传
    
    Args:
        file: 上传的CSV文件
        
    Returns:
        包含数据预览信息的字典
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="只支持CSV文件")
    
    temp_file = None
    try:
        # 创建临时文件
        content = await file.read()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_file.write(content)
        temp_file.close()  # 显式关闭文件
        
        # 加载CSV文件
        preview_data = data_loader.load_csv(temp_file.name)
        return {
            "status": "success",
            "data": preview_data
        }
    except DataLoadError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")
    finally:
        # 确保在最后清理临时文件
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass  # 忽略删除临时文件时的错误

@router.post("/upload/excel")
async def upload_excel(file: UploadFile = File(...)) -> Dict[str, Any]:
    """处理Excel文件上传
    
    Args:
        file: 上传的Excel文件
        
    Returns:
        包含数据预览信息的字典
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="只支持Excel文件")
    
    temp_file = None
    try:
        # 创建临时文件
        content = await file.read()
        suffix = '.xlsx' if file.filename.endswith('.xlsx') else '.xls'
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp_file.write(content)
        temp_file.close()  # 显式关闭文件
        
        # 加载Excel文件
        preview_data = data_loader.load_excel(temp_file.name)
        return {
            "status": "success",
            "data": preview_data
        }
    except DataLoadError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")
    finally:
        # 确保在最后清理临时文件
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass  # 忽略删除临时文件时的错误 