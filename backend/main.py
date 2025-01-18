from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pathlib import Path
from code_executor import CodeExecutor
import markdown2
from weasyprint import HTML
from jinja2 import Environment, BaseLoader
import tempfile

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

# 创建notebooks目录（如果不存在）
NOTEBOOKS_DIR = Path("notebooks")
NOTEBOOKS_DIR.mkdir(exist_ok=True)

# PDF模板
PDF_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @font-face {
            font-family: 'NotoSansSC';
            src: url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap');
        }
        
        body { 
            font-family: 'NotoSansSC', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        .cell { 
            margin: 20px 0; 
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            background: white;
        }
        .code { 
            background-color: #f8f9fa;
            padding: 15px;
            font-family: 'NotoSansSC', 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.5;
            border-radius: 4px;
            border: 1px solid #e9ecef;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .output { 
            margin-top: 10px;
            padding: 15px;
            background-color: #fff;
            border: 1px solid #e9ecef;
            border-radius: 4px;
        }
        .output pre {
            margin: 0;
            font-family: 'NotoSansSC', 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        img { 
            max-width: 100%;
            height: auto;
            margin: 10px 0;
            border-radius: 4px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            font-family: 'NotoSansSC', Arial, sans-serif;
        }
        /* Python语法高亮 */
        .python-string { 
            color: #067d17; 
            white-space: pre-wrap;
            word-break: break-all;
            word-wrap: break-word;
        }
        .python-comment { 
            color: #888; 
            font-style: italic;
            font-family: 'NotoSansSC', 'Consolas', 'Monaco', 'Courier New', monospace;
            white-space: pre-wrap;
            word-break: break-all;
            word-wrap: break-word;
        }
        .python-keyword { color: #0033b3; }
        .python-function { color: #7a7a2b; }
        .python-number { color: #1750eb; }
        
        /* 确保所有代码元素都能正确换行 */
        .code span {
            white-space: pre-wrap;
            word-break: break-all;
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    {% for cell in cells %}
        <div class="cell">
            {% if cell.type == 'code' %}
                <div class="code">{{ cell.content | format_python_code }}</div>
                {% if cell.output %}
                    <div class="output">
                        {% if cell.output.output %}
                            <pre>{{ cell.output.output }}</pre>
                        {% endif %}
                        {% if cell.output.plot %}
                            {{ cell.output.plot }}
                        {% endif %}
                    </div>
                {% endif %}
            {% else %}
                {{ cell.content_html }}
            {% endif %}
        </div>
    {% endfor %}
</body>
</html>
"""

# Python代码格式化函数
def format_python_code(code):
    import re
    from html import escape, unescape
    
    try:
        # 首先解码所有HTML实体
        code = unescape(code)
        
        # 标准化换行符
        code = code.replace('\r\n', '\n').replace('\r', '\n')
        
        # 将代码按行分割，分别处理每一行
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.rstrip()  # 移除行尾空白字符
            if not line:  # 处理空行
                formatted_lines.append('')
                continue
                
            # 检查是否包含注释
            comment_match = re.search(r'(#.*)$', line)
            if comment_match:
                # 分离代码和注释部分
                comment = comment_match.group(1)
                code_part = line[:comment_match.start()]
                
                # 处理代码部分
                if code_part.strip():
                    code_part = format_code_part(code_part.rstrip())
                
                # 处理注释部分（保留注释前的空格）
                space_before_comment = ' ' if code_part.strip() else ''
                comment = f'{space_before_comment}<span class="python-comment">{comment}</span>'
                
                # 组合代码和注释
                formatted_lines.append(code_part + comment)
            else:
                # 没有注释的行，直接处理代码
                formatted_lines.append(format_code_part(line))
        
        # 重新组合所有行
        return '<br>'.join(formatted_lines)
    except Exception as e:
        print(f"格式化代码时出错: {str(e)}")
        # 如果出错，返回解码后的原始代码
        return escape(unescape(code))  # 先解码再转义

def format_code_part(code):
    """处理代码部分的格式化"""
    import re
    from html import escape
    
    try:
        # 创建一个标记列表，记录每个位置的样式
        length = len(code)
        if length == 0:
            return ""
            
        styles = [set() for _ in range(length)]
        
        # 预处理：转义HTML特殊字符，但保留引号
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # 按顺序定义语法高亮规则
        patterns = [
            # 字符串（包括带引号的标签内容）
            (r'("(?:[^"\\]|\\.)*")', 'python-string'),
            (r"('(?:[^'\\]|\\.)*')", 'python-string'),
            # 列表中的方括号
            (r'(\[|\])', 'python-keyword'),
            # 数字（包括负数和小数）
            (r'(-?\d+\.?\d*)', 'python-number'),
            # 函数调用
            (r'([a-zA-Z_][a-zA-Z0-9_]*(?=\())', 'python-function'),
            # 关键字
            (r'\b(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b', 'python-keyword'),
        ]
        
        # 应用语法高亮规则
        for pattern, class_name in patterns:
            for match in re.finditer(pattern, code):
                try:
                    start, end = match.span()
                    # 确保索引在有效范围内
                    start = max(0, min(start, length - 1))
                    end = max(0, min(end, length))
                    
                    # 为匹配的范围添加样式
                    for i in range(start, end):
                        styles[i].add(class_name)
                except Exception as e:
                    print(f"处理模式 {pattern} 时出错: {str(e)}")
                    continue
        
        # 构建结果
        result = []
        current_styles = set()
        
        for i, char in enumerate(code):
            if i >= length:
                break
                
            # 检查样式变化
            new_styles = styles[i]
            
            # 如果样式发生变化，关闭旧的标签并打开新的标签
            if new_styles != current_styles:
                # 关闭旧的标签
                if current_styles:
                    result.append('</span>' * len(current_styles))
                # 打开新的标签
                if new_styles:
                    for style in new_styles:
                        result.append(f'<span class="{style}">')
                current_styles = new_styles
            
            result.append(char)
        
        # 关闭所有剩余的标签
        if current_styles:
            result.append('</span>' * len(current_styles))
        
        return ''.join(result)
    except Exception as e:
        print(f"格式化代码时出错: {str(e)}")
        return escape(code)  # 如果出错，返回转义后的原始代码

# 创建Jinja2环境并添加过滤器
jinja_env = Environment(loader=BaseLoader())
jinja_env.filters['format_python_code'] = format_python_code

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
        
        if not filename.endswith('.pdf'):
            filename += '.pdf'
            
        # 处理单元格内容
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
            
        # 渲染HTML模板
        template = jinja_env.from_string(PDF_TEMPLATE)
        html_content = template.render(
            title=filename.replace('.pdf', ''),
            cells=cells
        )
        
        # 创建临时HTML文件（使用二进制模式）
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='wb') as tmp_html:
            tmp_html.write(html_content.encode('utf-8'))
            tmp_html_path = tmp_html.name
            
        # 生成PDF，使用特定的字体配置
        pdf_path = NOTEBOOKS_DIR / filename
        HTML(tmp_html_path).write_pdf(
            str(pdf_path),
            stylesheets=[],
            presentational_hints=True,
            optimize_size=('fonts', 'images'),
            font_config=None  # 使用系统默认字体配置
        )
        
        # 删除临时HTML文件
        os.unlink(tmp_html_path)
        
        # 返回生成的PDF文件
        return FileResponse(
            path=str(pdf_path),
            media_type='application/pdf',
            filename=filename
        )
        
    except Exception as e:
        print(f"PDF导出错误: {str(e)}")  # 添加错误日志
        raise HTTPException(status_code=500, detail=str(e)) 