# API 模块管理

## 概述

为了更好地组织代码和提高可维护性，我们将所有与后端API交互的代码按功能模块进行了封装。每个功能模块都有对应的API文件，用于管理该模块的所有API调用。

## API 文件结构

目前，我们有以下API模块：

1. `http.js`: 基础HTTP请求封装，包含API端点配置和通用请求方法
2. `example_api.js`: 代码示例模块的API封装
3. `ai_api.js`: AI相关功能的API封装

## AI API (ai_api.js)

AI API模块封装了与AI相关的所有API调用，包括提示词管理和代码生成。

### 提示词管理

#### 系统提示词

系统提示词是用于配置AI代码生成的系统级提示词。

- `fetchSystemPrompts()`: 获取系统提示词列表
- `saveSystemPrompts(prompts)`: 保存系统提示词
- `resetSystemPrompts()`: 重置系统提示词为默认值

#### 用户提示词

用户提示词是用于配置AI代码生成的用户级要求。

- `fetchUserPrompts()`: 获取用户提示词列表
- `saveUserPrompts(requirements)`: 保存用户提示词
- `resetUserPrompts()`: 重置用户提示词为默认值

### 代码生成

- `generateCode(params)`: 根据用户提示词和数据框信息生成Python代码
  - `params.prompt`: 用户输入的提示词
  - `params.notebook_context`: 笔记本上下文
  - `params.dataframe_info`: DataFrame信息
  - `params.dataframe_name`: DataFrame名称

## 代码示例API (example_api.js)

代码示例API模块封装了与代码示例相关的所有API调用。

### 分类管理

- `fetchCategories()`: 获取所有代码示例分类
- `createCategory(categoryData)`: 创建新的代码示例分类
- `updateCategory(categoryId, categoryData)`: 更新代码示例分类

### 示例管理

- `fetchExamplesByCategory(categoryId)`: 获取指定分类下的所有代码示例
- `createExample(exampleData)`: 创建新的代码示例
- `updateExample(exampleId, exampleData)`: 更新代码示例
- `deleteExample(exampleId)`: 删除代码示例
- `saveFromCell(data)`: 从单元格保存代码示例

## 使用方法

在组件中使用这些API函数非常简单，只需导入所需的函数并调用即可：

```javascript
// 使用AI API
import { generateCode } from '@/api/ai_api'

// 生成代码
const handleGenerate = async () => {
  try {
    const response = await generateCode({
      prompt: '根据数据生成一个散点图',
      notebook_context: notebookContext,
      dataframe_info: dataFrameInfo,
      dataframe_name: 'df'
    })
    
    // 处理返回的代码
    console.log(response.code)
  } catch (error) {
    // 错误处理
  }
}
```

## 错误处理

所有API函数都包含了基本的错误处理逻辑，会在控制台输出错误信息，并将错误向上抛出，以便调用者可以进行更具体的错误处理。

## 维护与扩展

如果需要添加新的API调用，应遵循以下原则：

1. 按功能模块组织API文件
2. 为每个API函数提供清晰的命名和文档注释
3. 实现统一的错误处理机制
4. 保持代码风格的一致性

这种API管理方式使代码更加模块化和可维护，符合前端开发的最佳实践。 