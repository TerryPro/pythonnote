# 数据操作API

## 数据文件操作

### 1. 列出数据文件
- **端点**: `/api/data-files/list`
- **方法**: GET
- **描述**: 列出所有可用的数据文件
- **响应示例**:
```json
{
    "status": "success",
    "files": [
        {
            "name": "example.csv",
            "path": "example.csv",
            "size": 1024,
            "modified": 1612345678
        }
    ]
}
```

### 2. 删除数据文件
- **端点**: `/api/data-files/delete`
- **方法**: DELETE
- **参数**: 
  - `filename`: 要删除的文件名
- **响应示例**:
```json
{
    "status": "success",
    "message": "文件删除成功"
}
```

### 3. 上传CSV文件
- **端点**: `/api/data-files/upload/csv`
- **方法**: POST
- **描述**: 上传CSV格式的数据文件
- **请求体**: multipart/form-data
  - `file`: CSV文件
- **响应示例**:
```json
{
    "status": "success",
    "message": "文件上传成功",
    "data": {
        "file_path": "example.csv",
        "file_name": "example.csv",
        "file_size": 1024
    }
}
```

### 4. 上传Excel文件
- **端点**: `/api/data-files/upload/excel`
- **方法**: POST
- **描述**: 上传Excel格式的数据文件
- **请求体**: multipart/form-data
  - `file`: Excel文件(.xlsx或.xls)
- **响应示例**:
```json
{
    "status": "success",
    "message": "文件上传成功",
    "data": {
        "file_path": "example.xlsx",
        "file_name": "example.xlsx",
        "file_size": 1024
    }
}
```

### 5. 预览CSV文件
- **端点**: `/api/data-files/preview/csv`
- **方法**: GET
- **参数**:
  - `filename`: 文件名
- **描述**: 预览CSV文件内容
- **响应示例**:
```json
{
    "status": "success",
    "data": {
        "columns": ["col1", "col2"],
        "data": [
            {"col1": "value1", "col2": "value2"}
        ]
    }
}
```

### 6. 预览Excel文件
- **端点**: `/api/data-files/preview/excel`
- **方法**: GET
- **参数**:
  - `filename`: 文件名
  - `sheet_name`: 工作表名称（可选）
- **描述**: 预览Excel文件内容
- **响应示例**:
```json
{
    "status": "success",
    "data": {
        "sheets": ["Sheet1", "Sheet2"],
        "current_sheet": "Sheet1",
        "columns": ["col1", "col2"],
        "data": [
            {"col1": "value1", "col2": "value2"}
        ]
    }
}
```

### 7. 重命名数据文件
- **端点**: `/api/data-files/rename`
- **方法**: POST
- **描述**: 重命名数据文件
- **请求体**:
```json
{
    "old_filename": "old.csv",
    "new_filename": "new.csv"
}
```
- **响应示例**:
```json
{
    "status": "success",
    "message": "文件重命名成功",
    "data": {
        "old_path": "old.csv",
        "new_path": "new.csv"
    }
}
```

## 数据探索操作

### 1. 上传CSV文件进行探索
- **端点**: `/api/data-explorer/upload/csv`
- **方法**: POST
- **描述**: 上传CSV文件并返回数据预览
- **请求体**: multipart/form-data
  - `file`: CSV文件
- **响应示例**:
```json
{
    "status": "success",
    "data": {
        "preview": [...],
        "columns": [...],
        "summary": {...}
    }
}
```

### 2. 上传Excel文件进行探索
- **端点**: `/api/data-explorer/upload/excel`
- **方法**: POST
- **描述**: 上传Excel文件并返回数据预览
- **请求体**: multipart/form-data
  - `file`: Excel文件
- **响应示例**:
```json
{
    "status": "success",
    "data": {
        "preview": [...],
        "columns": [...],
        "summary": {...}
    }
}
```

## 错误处理

所有API都可能返回以下错误：

- 400: 请求参数错误（如文件格式不支持）
- 404: 文件不存在
- 500: 服务器内部错误

错误响应格式：
```json
{
    "status": "error",
    "detail": "错误描述"
}
```

## 注意事项

1. 文件上传大小限制为100MB
2. 支持的文件格式：
   - CSV: .csv
   - Excel: .xlsx, .xls
3. 文件名不能包含特殊字符
4. 预览数据默认返回前100行 