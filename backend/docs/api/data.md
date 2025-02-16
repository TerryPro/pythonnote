# 数据处理API

## 数据格式支持

我们的平台支持多种数据格式，包括：
- CSV
- Excel (.xlsx, .xls)
- JSON
- Parquet

## 数据清洗与转换

### 1. 数据清洗
- 提供去除空值、重复值的功能。
- 支持数据类型转换和格式化。

### 2. 数据转换
- 支持数据的聚合、分组和透视。
- 提供数据的合并、连接和拆分功能。

## 数据处理API端点

### 1. 上传数据文件
- **端点**: `/api/data/upload`
- **方法**: POST
- **描述**: 上传数据文件并进行初步处理。
- **请求体**: multipart/form-data
  - `file`: 数据文件
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

### 2. 数据预览
- **端点**: `/api/data/preview`
- **方法**: GET
- **参数**:
  - `filename`: 文件名
- **描述**: 预览数据文件内容。
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
   - JSON
   - Parquet
3. 文件名不能包含特殊字符
4. 预览数据默认返回前100行 