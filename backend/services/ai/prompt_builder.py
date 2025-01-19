"""
Prompt builder for AI code generation.
"""
from typing import Dict, List, Optional

class PromptBuilder:
    """提示词构建器类"""
    
    @staticmethod
    def build_code_generation_prompt(
        user_request: str,
        notebook_context: Optional[Dict] = None,
        dataframe_info: Optional[Dict] = None
    ) -> str:
        """
        构建代码生成提示词
        
        Args:
            user_request: 用户的自然语言请求
            notebook_context: 笔记本上下文信息
            dataframe_info: DataFrame相关信息
            
        Returns:
            str: 构建好的提示词
        """
        prompt_parts: List[str] = []
        
        # 添加系统说明
        prompt_parts.append(
            "你是一个Python数据分析专家，请根据以下信息生成符合PEP 8规范的Python代码。"
        )
        
        # 添加笔记本上下文
        if notebook_context:
            prompt_parts.append("\n当前笔记本环境：")
            if "imports" in notebook_context:
                prompt_parts.append("已导入的包：")
                prompt_parts.append("\n".join(notebook_context["imports"]))
            if "variables" in notebook_context:
                prompt_parts.append("\n当前定义的变量：")
                prompt_parts.append("\n".join(
                    f"- {name}: {type_}" 
                    for name, type_ in notebook_context["variables"].items()
                ))
        
        # 添加DataFrame信息
        if dataframe_info:
            prompt_parts.append("\n可用的DataFrame信息：")
            for df_name, df_info in dataframe_info.items():
                prompt_parts.append(f"\n{df_name}:")
                if "shape" in df_info:
                    prompt_parts.append(f"- 形状: {df_info['shape']}")
                if "columns" in df_info:
                    prompt_parts.append("- 列信息:")
                    for col, dtype in df_info["columns"].items():
                        prompt_parts.append(f"  - {col}: {dtype}")
        
        # 添加用户请求
        prompt_parts.append(f"\n用户需求：\n{user_request}")
        
        # 添加输出要求
        prompt_parts.append(
            "\n请生成符合以下要求的代码："
            "\n1. 代码必须是可执行的Python代码片段，不需要包含__main__方法"
            "\n2. 遵循PEP 8编码规范"
            "\n3. 包含必要的注释"
            "\n4. 使用已有的变量和DataFrame"
            "\n5. 处理可能的异常情况"
        )
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def extract_code_from_response(response: str) -> str:
        """
        从AI响应中提取代码
        
        Args:
            response: AI的响应文本
            
        Returns:
            str: 提取出的代码
        """
        # 如果响应中包含代码块标记，提取其中的代码
        if "```python" in response:
            code_blocks = response.split("```python")
            if len(code_blocks) > 1:
                code = code_blocks[1].split("```")[0]
                return code.strip()
        
        # 如果没有代码块标记，假设整个响应都是代码
        return response.strip() 