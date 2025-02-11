from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.pdf.exporter import NotebookPDFExporter
from app.core.config import settings

router = APIRouter(tags=["export"])

# 创建PDF导出器实例
pdf_exporter = NotebookPDFExporter(settings.EXPORT_DIR)

@router.post("/export_pdf")
async def export_pdf(request: Request):
    try:
        data = await request.json()
        notebook = data.get("notebook", {})
        filename = data.get("filename", "notebook.pdf")
        
        # 使用PDF导出器生成PDF文件
        pdf_path = pdf_exporter.export(notebook, filename)
        
        # 返回生成的PDF文件
        return FileResponse(
            path=str(pdf_path),
            media_type='application/pdf',
            filename=filename
        )
        
    except Exception as e:
        print(f"PDF导出错误: {str(e)}")  # 添加错误日志
        raise HTTPException(status_code=500, detail=str(e)) 