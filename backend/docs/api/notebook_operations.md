# 笔记本操作API

## 笔记本管理

### 1. 获取笔记本列表
- **端点**: `/api/notebooks/list_notebooks`
- **方法**: GET
- **描述**: 获取所有可用的Jupyter笔记本文件
- **响应示例**:
```json
[
    {
        "name": "Example.ipynb",
        "path": "Example.ipynb",
        "last_modified": 1612345678
    }
]
```

### 2. 保存笔记本
- **端点**: `/api/notebooks/save_notebook`
- **方法**: POST
- **描述**: 保存Jupyter笔记本内容
- **请求体**:
```json
{
    "filename": "Example.ipynb",
    "notebook": {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4
    }
}
```
- **响应示例**:
```json
{
    "status": "success"
}
```

### 3. 加载笔记本
- **端点**: `/api/notebooks/load_notebook`
- **方法**: GET
- **参数**:
  - `filename`: 笔记本文件名
- **描述**: 加载指定的Jupyter笔记本内容
- **响应示例**:
```json
{
    "cells": [],
    "metadata": {},
    "nbformat": 4,
    "nbformat_minor": 4
}
```

## 笔记本导出

### 1. 导出为PDF
- **端点**: `/api/export/export_pdf`
- **方法**: POST
- **描述**: 将笔记本导出为PDF文件
- **请求体**:
```json
{
    "notebook": {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4
    },
    "filename": "output.pdf"
}
```
- **响应**: 直接返回PDF文件流

## 错误处理

所有API都可能返回以下错误：

- 400: 请求参数错误
- 404: 笔记本文件不存在
- 500: 服务器内部错误

错误响应格式：
```json
{
    "status": "error",
    "detail": "错误描述"
}
```

## 注意事项

1. 笔记本文件必须是有效的.ipynb格式
2. 文件名不能包含特殊字符
3. PDF导出功能需要确保服务器安装了相应的依赖
4. 建议定期保存笔记本内容，避免数据丢失 