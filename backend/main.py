from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pathlib import Path
from code_executor import CodeExecutor
from services.pdf.code_formatter import format_python_code
from services.pdf.exporter import NotebookPDFExporter

app = FastAPI()
code_executor = CodeExecutor()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建必要的目录
NOTEBOOKS_DIR = Path("notebooks")
NOTEBOOKS_DIR.mkdir(exist_ok=True)

EXPORT_DIR = Path(__file__).parent / "export"
EXPORT_DIR.mkdir(exist_ok=True)

# 创建PDF导出器实例
pdf_exporter = NotebookPDFExporter(EXPORT_DIR)

@app.post("/execute")
async def execute_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    result = code_executor.execute(code)
    return result

@app.post("/reset_context")
async def reset_context():
    code_executor.reset()
    return {"status": "success"}

@app.get("/list_notebooks")
async def list_notebooks():
    notebooks = []
    for file in NOTEBOOKS_DIR.glob("*.ipynb"):
        notebooks.append({
            "name": file.name,
            "path": file.name,
            "last_modified": os.path.getmtime(file)
        })
    # 按最后修改时间排序
    notebooks.sort(key=lambda x: x["last_modified"], reverse=True)
    return notebooks

@app.post("/save_notebook")
async def save_notebook(request: Request):
    data = await request.json()
    filename = data.get("filename")
    notebook = data.get("notebook")
    
    if not filename or not notebook:
        return {"status": "error", "message": "Missing filename or notebook data"}
    
    file_path = NOTEBOOKS_DIR / filename
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)
    
    return {"status": "success"}

@app.get("/load_notebook")
async def load_notebook(filename: str):
    file_path = NOTEBOOKS_DIR / filename
    
    if not file_path.exists():
        return {"status": "error", "message": "Notebook not found"}
    
    with open(file_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
    
    return notebook 

@app.post("/export_pdf")
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