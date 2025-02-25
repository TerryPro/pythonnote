from fastapi import APIRouter, Request
from app.services.notebook.notebook_manager import NoteBookManager

notebook_manager = NoteBookManager() 

router = APIRouter(prefix="/api/notebooks", tags=["notebooks"])

@router.get("/list_notebooks")
async def list_notebooks_route():
    return notebook_manager.list_notebooks()

@router.post("/save_notebook")
async def save_notebook_route(request: Request):
    data = await request.json()
    filename = data.get("filename")
    notebook = data.get("notebook")
    return notebook_manager.save_notebook(filename, notebook)

@router.post("/rename_notebook")
async def rename_notebook_route(request: Request):
    data = await request.json()
    old_filename = data.get("old_filename")
    new_filename = data.get("new_filename")
    return notebook_manager.rename_notebook(old_filename, new_filename)

@router.delete("/delete_notebook")
async def delete_notebook_route(filename: str):
    return notebook_manager.delete_notebook(filename)

@router.get("/load_notebook")
async def load_notebook_route(filename: str):
    return notebook_manager.load_notebook(filename)