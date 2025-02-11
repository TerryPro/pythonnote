import tempfile
import os
from pathlib import Path
import markdown2
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Any, Optional
from .code_formatter import format_python_code

class NotebookPDFExporter:
    def __init__(self, export_dir: Path):
        """
        初始化PDF导出器
        
        Args:
            export_dir: PDF导出目录的Path对象
        """
        self.export_dir = export_dir
        
        # 创建Jinja2环境
        template_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        self.jinja_env.filters['format_python_code'] = format_python_code

    def process_cells(self, notebook: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        处理notebook中的单元格内容
        
        Args:
            notebook: notebook数据字典
            
        Returns:
            List[Dict[str, Any]]: 处理后的单元格列表
        """
        cells = []
        for cell in notebook.get("cells", []):
            cell_data = {
                "type": cell.get("type"),
                "content": cell.get("content", "")
            }
            
            if cell["type"] == "markdown":
                # 转换Markdown为HTML
                cell_data["content_html"] = markdown2.markdown(cell["content"])
            else:
                cell_data["output"] = cell.get("output", {})
                
            cells.append(cell_data)
        return cells

    def generate_html(self, cells: List[Dict[str, Any]], title: str) -> str:
        """
        生成HTML内容
        
        Args:
            cells: 处理后的单元格列表
            title: PDF文档标题
            
        Returns:
            str: 生成的HTML内容
        """
        template = self.jinja_env.get_template("notebook.html")
        return template.render(
            title=title,
            cells=cells
        )

    def create_temp_html(self, html_content: str) -> str:
        """
        创建临时HTML文件
        
        Args:
            html_content: HTML内容
            
        Returns:
            str: 临时文件路径
        """
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='wb') as tmp_html:
            tmp_html.write(html_content.encode('utf-8'))
            return tmp_html.name

    def generate_pdf(self, html_path: str, output_path: Path) -> None:
        """
        从HTML生成PDF文件
        
        Args:
            html_path: HTML文件路径
            output_path: PDF输出路径
        """
        HTML(html_path).write_pdf(
            str(output_path),
            stylesheets=[],
            presentational_hints=True,
            optimize_size=('fonts', 'images'),
            font_config=None  # 使用系统默认字体配置
        )

    def cleanup_temp_file(self, file_path: str) -> None:
        """
        清理临时文件
        
        Args:
            file_path: 要删除的文件路径
        """
        try:
            os.unlink(file_path)
        except Exception as e:
            print(f"清理临时文件时出错: {str(e)}")

    def export(self, notebook: Dict[str, Any], filename: str) -> Path:
        """
        导出notebook为PDF文件
        
        Args:
            notebook: notebook数据字典
            filename: 输出文件名
            
        Returns:
            Path: 生成的PDF文件路径
            
        Raises:
            Exception: 当PDF生成过程中出现错误时
        """
        if not filename.endswith('.pdf'):
            filename += '.pdf'

        try:
            # 处理单元格内容
            cells = self.process_cells(notebook)
            
            # 生成HTML内容
            html_content = self.generate_html(cells, filename.replace('.pdf', ''))
            
            # 创建临时HTML文件
            tmp_html_path = self.create_temp_html(html_content)
            
            try:
                # 生成PDF文件
                pdf_path = self.export_dir / filename
                self.generate_pdf(tmp_html_path, pdf_path)
                return pdf_path
                
            finally:
                # 清理临时文件
                self.cleanup_temp_file(tmp_html_path)
                
        except Exception as e:
            raise Exception(f"PDF导出失败: {str(e)}") 