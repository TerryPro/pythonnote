# API 概览

## 简介
本文档详细说明了数据分析助手后端提供的所有API接口。所有API都遵循RESTful设计原则，使用JSON格式进行数据交换。

## 基础信息
- 基础URL: `http://localhost:8000`
- API版本: v1.0.0
- 认证方式: Bearer Token

## API分类

### 1. [数据文件操作](data_operations.md)
- 文件上传下载
- 文件预览
- 文件管理

### 2. [DataFrame操作](dataframe_operations.md)
- DataFrame信息查询
- 数据预览
- 数据保存

### 3. [笔记本操作](notebook_operations.md)
- 笔记本管理
- 笔记本导出

## 通用规范

### 1. 请求格式
- GET请求：参数通过URL查询字符串传递
- POST请求：数据通过JSON格式在请求体中传递
- 文件上传：使用multipart/form-data格式

### 2. 响应格式
所有API响应都遵循以下格式：
```json
{
    "status": "success|error",
    "data": {},
    "message": "操作结果描述"
}
```

### 3. 错误处理
所有API使用标准的HTTP状态码：
- 200: 请求成功
- 400: 请求参数错误
- 401: 未认证
- 403: 未授权
- 404: 资源不存在
- 500: 服务器内部错误

错误响应格式：
```json
{
    "status": "error",
    "detail": "错误描述"
}
```

### 4. 认证
所有API请求需要在Header中包含认证Token：
```
Authorization: Bearer <your_token>
```

## 性能考虑

### 1. 数据处理
- 大文件上传建议分片
- 大数据集操作建议分批
- 预览功能会限制返回数据量

### 2. 并发处理
- 文件操作有并发限制
- DataFrame操作是内存中进行
- 导出功能可能需要较长时间

## 安全性

### 1. 文件操作
- 限制文件大小
- 校验文件类型
- 防止路径穿越

### 2. 数据访问
- 数据隔离
- 权限控制
- 敏感信息保护

## 最佳实践

1. 定期清理临时文件
2. 合理使用数据缓存
3. 处理大数据时注意内存使用
4. 及时保存重要数据
5. 使用异步操作处理耗时任务

## API端点列表

### 1. DataFrame操作

#### 1.1 获取DataFrame列表
- **端点**: `/api/dataframes/list`
- **方法**: GET
- **描述**: 获取所有可用的DataFrame变量名列表
- **响应示例**:
```json
{
    "status": "success",
    "data": ["df1", "df2", "df3"]
}
```

#### 1.2 获取DataFrame信息
- **端点**: `/api/dataframes/info/{name}`
- **方法**: GET
- **描述**: 获取指定DataFrame的详细信息
- **参数**:
  - `name`: DataFrame名称
- **响应示例**:
```json
{
    "basic_info": {
        "行数": 1000,
        "列数": 10,
        "内存占用": "1.2 MB"
    },
    "columns": [
        {
            "name": "column1",
            "type": "int64",
            "null_count": 0
        }
    ],
    "preview": {
        "head": [...],
        "summary": {...}
    }
}
```

### 2. AI服务

#### 2.1 生成代码
- **端点**: `/api/ai/generate_code`
- **方法**: POST
- **描述**: 根据提示词生成Python代码
- **请求体**:
```json
{
    "prompt": "计算数据的平均值",
    "dataframe_name": "df1",
    "notebook_context": {}
}
```
- **响应示例**:
```json
{
    "status": "success",
    "code": "df1['column'].mean()"
}
```

#### 2.2 获取系统提示词
- **端点**: `/api/ai/system-prompts`
- **方法**: GET
- **描述**: 获取当前系统提示词配置
- **响应示例**:
```json
{
    "prompts": [
        "你是一个数据分析助手...",
        "请生成Python代码..."
    ]
}
```

### 3. 数据文件操作

#### 3.1 保存DataFrame
- **端点**: `/api/dataframes/{name}/save`
- **方法**: POST
- **描述**: 将DataFrame保存为文件
- **请求体**:
```json
{
    "file_path": "data/output.csv",
    "file_type": "csv",
    "save_options": {
        "index": false
    }
}
```

## 错误处理

所有API都使用标准的HTTP状态码，并返回统一格式的错误响应：

```json
{
    "status": "error",
    "message": "错误描述",
    "code": "ERROR_CODE",
    "details": {}
}
```

常见状态码：
- 200: 请求成功
- 400: 请求参数错误
- 401: 未认证
- 403: 未授权
- 404: 资源不存在
- 500: 服务器内部错误

## 限流说明

- 普通接口: 60次/分钟
- AI生成接口: 10次/分钟

## 注意事项

1. 所有请求都需要包含认证token
2. 大数据量操作建议使用异步接口
3. 文件上传大小限制为100MB 