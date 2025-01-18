import re
from html import escape, unescape
from typing import List, Set

def format_python_code(code: str) -> str:
    """
    格式化Python代码，添加语法高亮
    
    Args:
        code: 要格式化的Python代码字符串
        
    Returns:
        str: 格式化后的HTML字符串，包含语法高亮
    """
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

def format_code_part(code: str) -> str:
    """
    处理代码部分的格式化，添加语法高亮
    
    Args:
        code: 要格式化的代码片段
        
    Returns:
        str: 格式化后的HTML字符串，包含语法高亮
    """
    try:
        # 创建一个标记列表，记录每个位置的样式
        length = len(code)
        if length == 0:
            return ""
            
        styles: List[Set[str]] = [set() for _ in range(length)]
        
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
        current_styles: Set[str] = set()
        
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